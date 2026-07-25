"""
Pytest unit test suite for UI Solution: beatriz_async_pipeline_builder_de9503.
"""
import pytest
from flose.solutions.beatriz_async_pipeline_builder_de9503 import BeatrizAsyncPipelineBuilderDe9503Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizAsyncPipelineBuilderDe9503Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizAsyncPipelineBuilderDe9503Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
