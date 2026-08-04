# tests/test_web_app.py

import asyncio
from flose.solutions.floseup_189_po_evil_boss_refatorar_src_flo_d5be26 import process_data, handle_item, fetch_data

async def test_process_data():
    data = [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25}
    ]
    processed_data = await process_data(data)
    expected = [
        {"ID": 1, "NAME": "ALICE", "AGE": 30},
        {"ID": 2, "NAME": "BOB", "AGE": 25}
    ]
    assert processed_data == expected

async def test_handle_item():
    item = {"id": 1, "name": "Alice", "age": 30}
    result = await handle_item(item)
    expected = {"ID": 1, "NAME": "ALICE", "AGE": 30}
    assert result == expected

async def test_fetch_data():
    data = await fetch_data()
    expected_ids = [1, 2]
    assert all(d["id"] in expected_ids for d in data)

if __name__ == "__main__":
    asyncio.run(asyncio.gather(
        test_process_data(),
        test_handle_item(),
        test_fetch_data()
    ))