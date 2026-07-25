"""
Pytest unit test suite for Async Performance: kan_9697_recrutamento_contrata_o_para_k_507ded.
"""
import pytest
import asyncio
from flose.solutions.kan_9697_recrutamento_contrata_o_para_k_507ded import Kan9697RecrutamentoContrataOParaK507dedSolution

def test_lru_cache_operations():
    cache = Kan9697RecrutamentoContrataOParaK507dedSolution(capacity=2, ttl_sec=10.0)
    cache.set("a", 100)
    cache.set("b", 200)
    assert cache.get("a") == 100
    cache.set("c", 300)
    assert cache.get("b") is None  # Descartado pelo LRU

@pytest.mark.asyncio
async def test_async_benchmark_latency():
    cache = Kan9697RecrutamentoContrataOParaK507dedSolution()
    res = await cache.async_benchmark_latency(iterations=5)
    assert res["total_ms"] > 0
    assert res["avg_latency_per_op_ms"] < 10.0
