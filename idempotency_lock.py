import asyncio

async def acquire_lock(key, lease_duration=30):
    # Simulate acquiring a lock
    await asyncio.sleep(1)
    return True

async def release_lock(key):
    # Simulate releasing a lock
    await asyncio.sleep(1)