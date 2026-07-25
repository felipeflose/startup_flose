"""
Pytest unit test suite for UI Solution: beatriz_pixel_perfect_css_engine_cac18a.
"""
import pytest
from flose.solutions.beatriz_pixel_perfect_css_engine_cac18a import BeatrizPixelPerfectCssEngineCac18aSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizPixelPerfectCssEngineCac18aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizPixelPerfectCssEngineCac18aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
