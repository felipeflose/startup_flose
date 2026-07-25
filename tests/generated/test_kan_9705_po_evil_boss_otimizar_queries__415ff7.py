"""
Pytest unit test suite for Async Performance: kan_9705_po_evil_boss_otimizar_queries__415ff7.
"""
import pytest
import asyncio
from flose.solutions.kan_9705_po_evil_boss_otimizar_queries__415ff7 import Kan9705PoEvilBossOtimizarQueries415ff7Solution

def test_lru_cache_operations():
    cache = Kan9705PoEvilBossOtimizarQueries415ff7Solution(capacity=2, ttl_sec=10.0)
    cache.set("a", 100)
    cache.set("b", 200)
    assert cache.get("a") == 100
    cache.set("c", 300)
    assert cache.get("b") is None  # Descartado pelo LRU

@pytest.mark.asyncio
async def test_async_benchmark_latency():
    cache = Kan9705PoEvilBossOtimizarQueries415ff7Solution()
    res = await cache.async_benchmark_latency(iterations=5)
    assert res["total_ms"] > 0
    assert res["avg_latency_per_op_ms"] < 10.0
