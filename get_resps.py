import aiohttp
import asyncio
import os
import json



def save_to_json(data):
    with open("resps.json", "w") as f:
        json.dump(data, f)


async def get_resps(session,url,nr):
    try:
        async with session.post(url, timeout=2400) as resp:

            print(nr,url)
            return await resp.json(),nr
    except:
        print("Warning something went wrong in asyncio_session")
        #return (False,False)

async def get_resps_from_urls(session,urls,nrs):
    tasks = []
    for url,nr in zip(urls,nrs):
        tasks.append(asyncio.create_task(get_resps(session,url,nr)))
    return await asyncio.gather(*tasks)

async def async_get_resps(urls,nrs):
    async with aiohttp.ClientSession() as session:
        return await get_resps_from_urls(session,urls,nrs)


def get(urls, nrs):
    return asyncio.run(async_get_resps(urls, nrs))
   

    


if __name__ == "__main__":
    pass