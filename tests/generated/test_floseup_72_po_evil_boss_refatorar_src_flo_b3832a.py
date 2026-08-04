from flose.solutions.floseup_72_po_evil_boss_refatorar_src_flo_b3832a import *
import pytest

async def mock_fetch_data():
    yield 'data1'
    yield 'data2'

@patch('flose.web_app.BackendProtocol.fetch_data', new_callable=mock_fetch_data)
def test_get_data(mock_fetch):
    backend = MagicMock(spec=BackendProtocol)
    async_typing = AsyncTyping(backend)
    result = await async_typing.get_data()
    assert result == ['data1', 'data2']
