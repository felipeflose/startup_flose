"""
Pytest unit test suite for Async Performance: kan_9847_po_frenzy_otimiza_o_de_perform_dcf25b.
"""
import pytest
import asyncio
from flose.solutions.kan_9847_po_frenzy_otimiza_o_de_perform_dcf25b import Kan9847PoFrenzyOtimizaODePerformDcf25bSolution

def test_lru_cache_operations():
    cache = Kan9847PoFrenzyOtimizaODePerformDcf25bSolution(capacity=2, ttl_sec=10.0)
    cache.set("a", 100)
    cache.set("b", 200)
    assert cache.get("a") == 100
    cache.set("c", 300)
    assert cache.get("b") is None  # Descartado pelo LRU

@pytest.mark.asyncio
async def test_async_benchmark_latency():
    cache = Kan9847PoFrenzyOtimizaODePerformDcf25bSolution()
    res = await cache.async_benchmark_latency(iterations=5)
    assert res["total_ms"] > 0
    assert res["avg_latency_per_op_ms"] < 10.0
