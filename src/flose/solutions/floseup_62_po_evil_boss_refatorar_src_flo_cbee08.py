from typing import List, Dict, Any, Awaitable, Coroutine

async def process_data(data: List[Dict[str, Any]]) -> Awaitable[List[Dict[str, Any]]]:
    processed_data = []
    for item in data:
        # Simulate asynchronous processing
        await asyncio.sleep(0.1)
        processed_item = {key: value * 2 for key, value in item.items()}
        processed_data.append(processed_item)
    return processed_data