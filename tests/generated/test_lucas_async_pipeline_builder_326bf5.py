"""
Pytest unit test suite for UI Solution: lucas_async_pipeline_builder_326bf5.
"""
import pytest
from flose.solutions.lucas_async_pipeline_builder_326bf5 import LucasAsyncPipelineBuilder326bf5Solution

def test_hex_to_hsl_conversion():
    sol = LucasAsyncPipelineBuilder326bf5Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = LucasAsyncPipelineBuilder326bf5Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
