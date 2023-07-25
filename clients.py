import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        print("create")
        response = await session.post(
            "http://127.0.0.1:8080/users/", json={"name": "user_2", "password": "1234"}
        )
        print(response.status)

        response = await session.get(
            "http://127.0.0.1:8080/users/3",
        )
        print(response.status)
        json_data = await response.json()
        print(json_data)


        response = await session.post(
            "http://127.0.0.1:8080/users/", json={"name": "user_2", "password": "1234"}
        )
        print(response.status)

        # print("delete")
        # response = await session.delete(
        #     "http://127.0.0.1:8080/users/1",
        # )
        # print(response.status)
        # json_data = await response.json()
        # print(json_data)

asyncio.run(main())