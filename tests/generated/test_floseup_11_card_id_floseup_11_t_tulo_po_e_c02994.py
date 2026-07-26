"""
Pytest unit test suite for Async Performance: floseup_11_card_id_floseup_11_t_tulo_po_e_c02994.
"""
import pytest
import asyncio
from flose.solutions.floseup_11_card_id_floseup_11_t_tulo_po_e_c02994 import Floseup11CardIdFloseup11TTuloPoEC02994Solution

def test_lru_cache_operations():
    cache = Floseup11CardIdFloseup11TTuloPoEC02994Solution(capacity=2, ttl_sec=10.0)
    cache.set("a", 100)
    cache.set("b", 200)
    assert cache.get("a") == 100
    cache.set("c", 300)
    assert cache.get("b") is None  # Descartado pelo LRU

@pytest.mark.asyncio
async def test_async_benchmark_latency():
    cache = Floseup11CardIdFloseup11TTuloPoEC02994Solution()
    res = await cache.async_benchmark_latency(iterations=5)
    assert res["total_ms"] > 0
    assert res["avg_latency_per_op_ms"] < 10.0
