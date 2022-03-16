import os
import argparse

import asyncio
import aiohttp


async def get_url(session, url, path, filename):
    async with session.get(url) as response:
        r = await response.read()
        with open(f"{path}/{filename}.jpeg", 'wb') as f:
            f.write(r)


async def get_url_list(url, count, path):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(get_url(session, url, path, i)) for i in range(count)]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, help='count', default=10)
    parser.add_argument('-p', type=str, help='save_path', default='artefacts/easy')
    args = parser.parse_args()

    os.makedirs(args.p, exist_ok=True)
    url = 'https://picsum.photos/200/300'

    asyncio.run(get_url_list(url, args.n, args.p))