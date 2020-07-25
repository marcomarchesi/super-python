'''
web scraper
'''

import requests
from multiprocessing import Pool
import concurrent.futures
import time
import sys

def generate_urls(base_url, size):
    urls = []
    for i in range(size):
        urls.append(base_url + str(i+1))
    return urls

def scrape(url):
    res = requests.get(url)
    print(res.status_code, res.url)

def use_threads(function, argument):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(function, argument)
    print("Multithreading - Time elapsed: %s" % str(time.time() - start_time))

def func(x):
    return x*x

def use_multiprocessing(function, argument):
    # with Pool in a context manager we don't need to terminate or join it
    # urls are not scraped in order
    with Pool(5) as p:
        p.map(scrape, urls)

def use_apply(p):
    # it runs only on one worker. It needs the function and the iterable arguments. No need for get() as it returns the value
    res = p.apply(func, (20,))
    print(res) #400

def use_apply_async(p):
    # it runs only on one worker. It needs the function and the iterable arguments
    res = p.apply_async(func, (20,))
    print(res.get()) #400



if __name__ == "__main__":
    urls = generate_urls('http://quotes.toscrape.com/page/', 10)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'thread':
            use_threads(scrape, urls)
        else:
            with Pool(5) as p:
                if sys.argv[1] == 'apply':
                    use_apply(p)
                if sys.argv[1] == 'apply async':
                    use_apply_async(p)
    else:
        use_multiprocessing(scrape, urls)



# we can run with `time python web_scraper.py`


