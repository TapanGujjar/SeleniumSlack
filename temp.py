import asyncio
import time
from codetiming import Timer
def task(name, work_queue):
    # timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
    # while not work_queue.empty():
        # delay = await work_queue.get()
    print(f"Task {name} running and sleeping for 10 seconds") 
    # timer.start()
    # await asyncio.sleep(delay)
    time.sleep(10)
        # timer.stop()


async def main():
    """
    This is the main entry point for the program
    """
    # Create the queue of work
    work_queue = asyncio.Queue()
    # Put some work in the queue
    for work in [15, 10, 5, 2]:
        await work_queue.put(work)

    # Run the tasks
    # with Timer(text="\nTotal elapsed time: {:.1f}"):
    await asyncio.gather(
        asyncio.create_task(task("One", work_queue)),
        asyncio.create_task(task("Two", work_queue)),
    )

def test():
    asyncio.run(main())

test()