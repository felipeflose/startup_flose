"""
Pytest unit test suite for UI Solution: sofia_async_pipeline_builder_da3113.
"""
import pytest
from flose.solutions.sofia_async_pipeline_builder_da3113 import SofiaAsyncPipelineBuilderDa3113Solution

def test_hex_to_hsl_conversion():
    sol = SofiaAsyncPipelineBuilderDa3113Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaAsyncPipelineBuilderDa3113Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
