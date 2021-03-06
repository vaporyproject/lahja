import asyncio
from typing import (
    AsyncGenerator,
    Tuple,
)

import pytest

from lahja import (
    Endpoint,
    EventBus,
)

EndpointPair = Tuple[Endpoint, Endpoint]
EndpointTriplet = Tuple[Endpoint, Endpoint, Endpoint]


@pytest.fixture(scope='function')
async def endpoint(event_loop: asyncio.AbstractEventLoop) -> AsyncGenerator[Endpoint, None]:
    bus = EventBus()
    endpoint = bus.create_endpoint('test')
    bus.start(event_loop)
    await endpoint.connect(event_loop)
    try:
        yield endpoint
    finally:
        endpoint.stop()
        bus.stop()


@pytest.fixture(scope='function')
async def pair_of_endpoints(event_loop: asyncio.AbstractEventLoop
                            ) -> AsyncGenerator[EndpointPair, None]:

    bus = EventBus()
    endpoint1 = bus.create_endpoint('e1')
    endpoint2 = bus.create_endpoint('e2')
    bus.start(event_loop)
    await endpoint1.connect(event_loop)
    await endpoint2.connect(event_loop)
    try:
        yield endpoint1, endpoint2
    finally:
        endpoint1.stop()
        endpoint2.stop()
        bus.stop()


@pytest.fixture(scope="function")
async def triplet_of_endpoints(event_loop: asyncio.AbstractEventLoop
                               ) -> AsyncGenerator[EndpointTriplet, None]:

    bus = EventBus()
    endpoint1 = bus.create_endpoint("e1")
    endpoint2 = bus.create_endpoint("e2")
    endpoint3 = bus.create_endpoint("e3")
    bus.start(event_loop)
    await endpoint1.connect(event_loop)
    await endpoint2.connect(event_loop)
    await endpoint3.connect(event_loop)
    try:
        yield endpoint1, endpoint2, endpoint3
    finally:
        endpoint1.stop()
        endpoint2.stop()
        endpoint3.stop()
        bus.stop()
