"""
Pytest unit test suite for UI Solution: sofia_pixel_perfect_css_engine_a73e71.
"""
import pytest
from flose.solutions.sofia_pixel_perfect_css_engine_a73e71 import SofiaPixelPerfectCssEngineA73e71Solution

def test_hex_to_hsl_conversion():
    sol = SofiaPixelPerfectCssEngineA73e71Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaPixelPerfectCssEngineA73e71Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
