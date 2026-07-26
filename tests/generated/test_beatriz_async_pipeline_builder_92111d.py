"""
Pytest unit test suite for UI Solution: beatriz_async_pipeline_builder_92111d.
"""
import pytest
from flose.solutions.beatriz_async_pipeline_builder_92111d import BeatrizAsyncPipelineBuilder92111dSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizAsyncPipelineBuilder92111dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizAsyncPipelineBuilder92111dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
