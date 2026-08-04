import pytest
from flose.solutions.floseup_62_po_evil_boss_refatorar_src_flo_cbee08 import process_data

@pytest.mark.asyncio
async def test_process_data():
    data = [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}]
    expected_output = [{'a': 2, 'b': 4}, {'c': 6, 'd': 8}]
    output = await process_data(data)
    assert output == expected_output