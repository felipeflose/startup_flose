"""
Pytest unit test suite for UI Solution: beatriz_async_pipeline_builder_4bafb4.
"""
import pytest
from flose.solutions.beatriz_async_pipeline_builder_4bafb4 import BeatrizAsyncPipelineBuilder4bafb4Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizAsyncPipelineBuilder4bafb4Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizAsyncPipelineBuilder4bafb4Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
