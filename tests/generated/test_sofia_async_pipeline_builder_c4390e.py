"""
Pytest unit test suite for UI Solution: sofia_async_pipeline_builder_c4390e.
"""
import pytest
from flose.solutions.sofia_async_pipeline_builder_c4390e import SofiaAsyncPipelineBuilderC4390eSolution

def test_hex_to_hsl_conversion():
    sol = SofiaAsyncPipelineBuilderC4390eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaAsyncPipelineBuilderC4390eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
