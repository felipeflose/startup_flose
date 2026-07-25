"""
Pytest unit test suite for UI Solution: beatriz_pixel_perfect_css_engine_ceeec1.
"""
import pytest
from flose.solutions.beatriz_pixel_perfect_css_engine_ceeec1 import BeatrizPixelPerfectCssEngineCeeec1Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizPixelPerfectCssEngineCeeec1Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizPixelPerfectCssEngineCeeec1Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
