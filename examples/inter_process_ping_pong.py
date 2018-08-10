import asyncio
import multiprocessing
import time

from lahja.eventbus import (
    Endpoint,
    EventBus,
    BaseEvent
)

PROC1_FIRED = "proc1_fired"
PROC2_FIRED = "proc2_fired"

class FirstThingHappened(BaseEvent):
    pass

class SecondThingHappened(BaseEvent):
    pass


def run_proc1(endpoint):
    loop = asyncio.get_event_loop()
    endpoint.connect()
    endpoint.subscribe(SecondThingHappened, lambda event: 
        print("Received via SUBSCRIBE API in proc1: ", event.payload)
    )
    endpoint.subscribe(FirstThingHappened, lambda event: 
        print("Receiving own event: ", event.payload)
    )

    loop.run_until_complete(proc1_worker(endpoint))

async def proc1_worker(endpoint):
    while True:
        print("Hello from proc1")
        if is_nth_second(5):
            endpoint.broadcast(
                FirstThingHappened("Hit from proc1 ({})".format(time.time()))
            )
        await asyncio.sleep(1)


def run_proc2(endpoint):
    loop = asyncio.get_event_loop()
    endpoint.connect()
    endpoint.subscribe(FirstThingHappened, lambda event: 
        print("Received via SUBSCRIBE API in proc2:", event.payload)
    )
    asyncio.ensure_future(display_proc1_events(endpoint))

    loop.run_until_complete(proc2_worker(endpoint))


async def proc2_worker(endpoint):
    while True:
        print("Hello from proc2")
        if is_nth_second(2):
            endpoint.broadcast(
                SecondThingHappened("Hit from proc2 ({})".format(time.time()))
            )
        await asyncio.sleep(1)

async def display_proc1_events(endpoint):
    async for event in endpoint.stream(FirstThingHappened):
        print("Received via STREAM API in proc2: ", event.payload)

def is_nth_second(interval):
    return int(time.time()) % interval is 0

if __name__ == "__main__":
    event_bus = EventBus()
    e1 = event_bus.create_endpoint('e1')
    e2 = event_bus.create_endpoint('e2')
    event_bus.start()

    p1 = multiprocessing.Process(target=run_proc1, args=(e1,))
    p1.start()

    p2 = multiprocessing.Process(target=run_proc2, args=(e2,))
    p2.start()
