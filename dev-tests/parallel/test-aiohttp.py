import aiohttp
import asyncio

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://python.org') as response:
#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#             html = await response.text()
#             print("Body:", html[:15], "...")

# asyncio.run(main())

async def fetch(session, url):
    async with session.get(url) as response:
        print(f"Status: {url} {response.status}")
        print(f"Content-type: {url} {response.headers['content-type']}")
        return await response.text()

async def main():
    urls = [
        'http://python.org',
        'https://google.com',
        'http://yifei.me'
    ]
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            tasks.append(fetch(session, url))
        htmls = await asyncio.gather(*tasks)
        for html in htmls:
            print(html[:100])

# if __name__ == '__main__':
loop = asyncio.new_event_loop()
loop.run_until_complete(main())
