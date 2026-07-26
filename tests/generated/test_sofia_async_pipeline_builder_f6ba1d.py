"""
Pytest unit test suite for UI Solution: sofia_async_pipeline_builder_f6ba1d.
"""
import pytest
from flose.solutions.sofia_async_pipeline_builder_f6ba1d import SofiaAsyncPipelineBuilderF6ba1dSolution

def test_hex_to_hsl_conversion():
    sol = SofiaAsyncPipelineBuilderF6ba1dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaAsyncPipelineBuilderF6ba1dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
