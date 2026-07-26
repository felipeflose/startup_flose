"""
Pytest unit test suite for UI Solution: felipe_async_pipeline_builder_01508c.
"""
import pytest
from flose.solutions.felipe_async_pipeline_builder_01508c import FelipeAsyncPipelineBuilder01508cSolution

def test_hex_to_hsl_conversion():
    sol = FelipeAsyncPipelineBuilder01508cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = FelipeAsyncPipelineBuilder01508cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
