import json

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

import config
from aiohttp import web
from auth import hash_password
from models import ORM_MODEL_CLS, Ads, Base, User

app = web.Application()
engine = create_async_engine(config.PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_items(session: Session, model_cls: ORM_MODEL_CLS, item_id: int | str):
    item = await session.get(model_cls, item_id)
    if item is None:
        raise web.HTTPNotFound(
            text=json.dumps({"error": "user not found"}),
            content_type="application/json",
        )
    return item


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request["session"] = session
        response = await handler(request)
        return response


class AdsViews(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def ads_id(self):
        return int(self.request.match_info["ads_id"])

    async def get(self):
        ads = await get_items(self.session, Ads, self.ads_id)
        return web.json_response({"id": ads.id, "title": ads.title, "autor": ads.autor})

    async def post(self):
        new_ads = await self.request.json()
        ads = Ads(**new_ads)
        self.session.add(ads)
        await self.session.commit()
        return web.json_response({"id": ads.id})

    async def patch(self):
        js_data = await self.request.json()
        ads = await get_items(self.session, Ads, self.ads_id)
        for fields, value in js_data.items():
            setattr(ads, fields, value)
        try:
            self.session.add(ads)
            await self.session.commit()
        except IntegrityError as er:
            raise web.HTTPConflict(
                text=json.dumps({"error": "ads already exists"}),
                content_type="application/json",
            )
        return web.json_response({"answer": "data changed"})

    async def delete(self):
        ads = await get_items(self.session, Ads, self.ads_id)
        await self.session.delete(ads)
        await self.session.commit()
        return web.json_response({"id": ads.id})


class UserViews(web.View):
    @property
    def session(self):
        return self.request["session"]

    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    async def get(self):
        user = await get_items(self.session, User, self.user_id)
        return web.json_response(
            {
                "id": user.id,
                "name": user.name,
                "creation_time": int(user.registration_time.timestamp()),
            }
        )

    async def post(self):
        new_user = await self.request.json()
        new_user["password"] = hash_password(new_user["password"])
        user = User(**new_user)
        self.session.add(user)
        await self.session.commit()
        return web.json_response({"id": user.id})

    async def delete(self):
        user = await get_items(self.session, User, self.user_id)
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"id": user.id})


async def orm_context(app: web.Application):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)
app.add_routes(
    [
        web.post("/users/", UserViews),
        web.get("/users/{user_id:\d+}", UserViews),
        web.patch("/users/{user_id:\d+}", UserViews),
        web.delete("/users/{user_id:\d+}", UserViews),
        web.post("/ads/", AdsViews),
        web.get("/ads/{ads_id:\d+}", AdsViews),
        web.patch("/ads/{ads_id:\d+}", AdsViews),
        web.delete("/ads/{ads_id:\d+}", AdsViews),
    ]
)


if __name__ == "__main__":
    web.run_app(app)
