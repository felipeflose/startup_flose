"""
Pytest unit test suite for UI Solution: sofia_pixel_perfect_css_engine_11f70a.
"""
import pytest
from flose.solutions.sofia_pixel_perfect_css_engine_11f70a import SofiaPixelPerfectCssEngine11f70aSolution

def test_hex_to_hsl_conversion():
    sol = SofiaPixelPerfectCssEngine11f70aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaPixelPerfectCssEngine11f70aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
