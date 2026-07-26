"""
Pytest unit test suite for General Solution: beatriz_ollama_quantization_26fa26.
"""
import pytest
import asyncio
from flose.solutions.beatriz_ollama_quantization_26fa26 import BeatrizOllamaQuantization26fa26Solution

def test_execute_refactoring():
    eng = BeatrizOllamaQuantization26fa26Solution(agent="Beatriz")
    res = eng.execute_refactoring("core_bus", ["async_opt", "type_hints"])
    assert res["code_quality_score"] == 98.5
    assert len(res["rules_applied"]) == 2

@pytest.mark.asyncio
async def test_validate_dag_pipeline():
    eng = BeatrizOllamaQuantization26fa26Solution()
    valid = await eng.async_validate_dag_pipeline()
    assert valid is True
