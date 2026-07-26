"""
Pytest unit test suite for UI Solution: sofia_async_pipeline_builder_b01d5d.
"""
import pytest
from flose.solutions.sofia_async_pipeline_builder_b01d5d import SofiaAsyncPipelineBuilderB01d5dSolution

def test_hex_to_hsl_conversion():
    sol = SofiaAsyncPipelineBuilderB01d5dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaAsyncPipelineBuilderB01d5dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
