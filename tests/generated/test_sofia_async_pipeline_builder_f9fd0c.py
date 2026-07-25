"""
Pytest unit test suite for UI Solution: sofia_async_pipeline_builder_f9fd0c.
"""
import pytest
from flose.solutions.sofia_async_pipeline_builder_f9fd0c import SofiaAsyncPipelineBuilderF9fd0cSolution

def test_hex_to_hsl_conversion():
    sol = SofiaAsyncPipelineBuilderF9fd0cSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaAsyncPipelineBuilderF9fd0cSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
