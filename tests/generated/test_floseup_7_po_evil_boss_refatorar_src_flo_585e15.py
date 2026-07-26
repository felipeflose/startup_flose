"""
Pytest unit test suite for UI Solution: floseup_7_po_evil_boss_refatorar_src_flo_585e15.
"""
import pytest
from flose.solutions.floseup_7_po_evil_boss_refatorar_src_flo_585e15 import Floseup7PoEvilBossRefatorarSrcFlo585e15Solution

def test_hex_to_hsl_conversion():
    sol = Floseup7PoEvilBossRefatorarSrcFlo585e15Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup7PoEvilBossRefatorarSrcFlo585e15Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
