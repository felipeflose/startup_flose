"""
Pytest unit test suite for General Solution: sofia_ollama_quantization_401b29.
"""
import pytest
import asyncio
from flose.solutions.sofia_ollama_quantization_401b29 import SofiaOllamaQuantization401b29Solution

def test_execute_refactoring():
    eng = SofiaOllamaQuantization401b29Solution(agent="Sofia")
    res = eng.execute_refactoring("core_bus", ["async_opt", "type_hints"])
    assert res["code_quality_score"] == 98.5
    assert len(res["rules_applied"]) == 2

@pytest.mark.asyncio
async def test_validate_dag_pipeline():
    eng = SofiaOllamaQuantization401b29Solution()
    valid = await eng.async_validate_dag_pipeline()
    assert valid is True
