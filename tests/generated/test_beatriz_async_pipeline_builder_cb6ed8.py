"""
Pytest unit test suite for UI Solution: beatriz_async_pipeline_builder_cb6ed8.
"""
import pytest
from flose.solutions.beatriz_async_pipeline_builder_cb6ed8 import BeatrizAsyncPipelineBuilderCb6ed8Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizAsyncPipelineBuilderCb6ed8Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizAsyncPipelineBuilderCb6ed8Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
