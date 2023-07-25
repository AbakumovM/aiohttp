import asyncio

import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        # print("create user")
        # response = await session.post(
        #     "http://127.0.0.1:8080/users/", json={"name": "user_3", "password": "1234"}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("get user")
        # response = await session.get(
        #     "http://127.0.0.1:8080/users/3",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("create ads")
        # response = await session.post(
        #     "http://127.0.0.1:8080/ads/", json={"title": 'World1', 'description': 'i love world',  'autor': 3}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("get user")
        # response = await session.get(
        #     "http://127.0.0.1:8080/ads/3",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)
        # print("patch ads")
        # response = await session.patch(
        #     "http://127.0.0.1:8080/ads/3", json={"title": "fix"}
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        # print("delete users")

        # response = await session.delete(
        #     "http://127.0.0.1:8080/users/1",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

        print("delete ads")
        response = await session.delete(
            "http://127.0.0.1:8080/users/3",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)


asyncio.run(main())
