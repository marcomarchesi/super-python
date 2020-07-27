'''
asyncio_web_scraper.py
'''

import asyncio
import aiohttp
import logging

def generate_urls(base_url, size):
    urls = []
    for i in range(size):
        urls.append(base_url + str(i+1))
    return urls

# coroutine
async def from_url(session, url):
    async with session.get(url) as response:
        logging.info("Read {0} from {1}".format(response.content_length, url))

# coroutine
async def scrape(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            # create the tasks
            task = asyncio.ensure_future(from_url(session, url)) #otherwise asyncio.create_task
            tasks.append(task)
        # group all the tasks
        await asyncio.gather(*tasks, return_exceptions=True)
                
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    urls = generate_urls('http://quotes.toscrape.com/page/', 10)
    # run the eventloop (from Python 3.7)
    asyncio.run(scrape(urls))
