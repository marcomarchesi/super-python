'''
async_io_example.py
'''
import logging
import asyncio
import time

logging.basicConfig(level=logging.INFO)

# coroutine
async def do_something(seq):
    await asyncio.sleep(max(seq))
    logging.info("task with seq {} is done".format(seq))
    return list(reversed(seq))

async def main():
    tasks = []
    # TODO: Test with create_task() and ensure_future() instead of directly call the coroutine
    tasks.append(do_something([3,2,1]))
    tasks.append(do_something([5,2,3]))
    tasks.append(do_something([2,1,2]))
    await asyncio.gather(*tasks)
    # print(t.result())

if __name__ == "__main__":
    asyncio.run(main())