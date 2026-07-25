"""
Pytest unit test suite for UI Solution: beatriz_pixel_perfect_css_engine_0d968b.
"""
import pytest
from flose.solutions.beatriz_pixel_perfect_css_engine_0d968b import BeatrizPixelPerfectCssEngine0d968bSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizPixelPerfectCssEngine0d968bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizPixelPerfectCssEngine0d968bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
