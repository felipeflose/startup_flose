"""
Pytest unit test suite for UI Solution: sofia_async_pipeline_builder_d41121.
"""
import pytest
from flose.solutions.sofia_async_pipeline_builder_d41121 import SofiaAsyncPipelineBuilderD41121Solution

def test_hex_to_hsl_conversion():
    sol = SofiaAsyncPipelineBuilderD41121Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaAsyncPipelineBuilderD41121Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
