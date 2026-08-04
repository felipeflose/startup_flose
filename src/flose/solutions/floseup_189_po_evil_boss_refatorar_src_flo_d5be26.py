# src/flose/web_app.py

import asyncio
from typing import Any, Dict, List

async def process_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for item in data:
        result = await handle_item(item)
        results.append(result)
    return results

async def handle_item(item: Dict[str, Any]) -> Dict[str, Any]:
    # Simulate some processing
    processed_data = {k: v.upper() if isinstance(v, str) else v for k, v in item.items()}
    await asyncio.sleep(0.1)  # Simulate async operation
    return processed_data

async def fetch_data():
    # Simulate data fetching
    await asyncio.sleep(0.2)
    return [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25}
    ]

async def main():
    data = await fetch_data()
    processed_data = await process_data(data)
    print(processed_data)

if __name__ == "__main__":
    asyncio.run(main())