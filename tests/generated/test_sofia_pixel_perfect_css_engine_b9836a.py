"""
Pytest unit test suite for UI Solution: sofia_pixel_perfect_css_engine_b9836a.
"""
import pytest
from flose.solutions.sofia_pixel_perfect_css_engine_b9836a import SofiaPixelPerfectCssEngineB9836aSolution

def test_hex_to_hsl_conversion():
    sol = SofiaPixelPerfectCssEngineB9836aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaPixelPerfectCssEngineB9836aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
