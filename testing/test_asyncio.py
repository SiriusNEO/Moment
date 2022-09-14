import asyncio

from frontend.frontend_config import SEND_WAIT

async def test():
    print("1")
    await asyncio.sleep(SEND_WAIT)
    print("2")

asyncio.run(test())