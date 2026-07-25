"""
Pytest unit test suite for General Solution: sofia_ollama_quantization_f40a28.
"""
import pytest
import asyncio
from flose.solutions.sofia_ollama_quantization_f40a28 import SofiaOllamaQuantizationF40a28Solution

def test_execute_refactoring():
    eng = SofiaOllamaQuantizationF40a28Solution(agent="Sofia")
    res = eng.execute_refactoring("core_bus", ["async_opt", "type_hints"])
    assert res["code_quality_score"] == 98.5
    assert len(res["rules_applied"]) == 2

@pytest.mark.asyncio
async def test_validate_dag_pipeline():
    eng = SofiaOllamaQuantizationF40a28Solution()
    valid = await eng.async_validate_dag_pipeline()
    assert valid is True
