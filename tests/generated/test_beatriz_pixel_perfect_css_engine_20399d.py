"""
Pytest unit test suite for UI Solution: beatriz_pixel_perfect_css_engine_20399d.
"""
import pytest
from flose.solutions.beatriz_pixel_perfect_css_engine_20399d import BeatrizPixelPerfectCssEngine20399dSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizPixelPerfectCssEngine20399dSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizPixelPerfectCssEngine20399dSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
