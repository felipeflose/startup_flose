"""
Pytest unit test suite for UI Solution: beatriz_pixel_perfect_css_engine_4fc0c6.
"""
import pytest
from flose.solutions.beatriz_pixel_perfect_css_engine_4fc0c6 import BeatrizPixelPerfectCssEngine4fc0c6Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizPixelPerfectCssEngine4fc0c6Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizPixelPerfectCssEngine4fc0c6Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
