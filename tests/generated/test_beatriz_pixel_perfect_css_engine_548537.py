"""
Pytest unit test suite for UI Solution: beatriz_pixel_perfect_css_engine_548537.
"""
import pytest
from flose.solutions.beatriz_pixel_perfect_css_engine_548537 import BeatrizPixelPerfectCssEngine548537Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizPixelPerfectCssEngine548537Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizPixelPerfectCssEngine548537Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
