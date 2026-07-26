"""
Pytest unit test suite for UI Solution: sofia_pixel_perfect_css_engine_c0229a.
"""
import pytest
from flose.solutions.sofia_pixel_perfect_css_engine_c0229a import SofiaPixelPerfectCssEngineC0229aSolution

def test_hex_to_hsl_conversion():
    sol = SofiaPixelPerfectCssEngineC0229aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaPixelPerfectCssEngineC0229aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
