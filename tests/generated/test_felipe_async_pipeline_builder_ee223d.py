"""
Pytest unit test suite for UI Solution: felipe_async_pipeline_builder_ee223d.
"""
import pytest
from flose.solutions.felipe_async_pipeline_builder_ee223d import FelipeAsyncPipelineBuilderEe223dSolution

def test_hex_to_hsl_conversion():
    sol = FelipeAsyncPipelineBuilderEe223dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = FelipeAsyncPipelineBuilderEe223dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
