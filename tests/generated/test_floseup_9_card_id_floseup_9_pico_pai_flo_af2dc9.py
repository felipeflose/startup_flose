"""
Pytest unit test suite for UI Solution: floseup_9_card_id_floseup_9_pico_pai_flo_af2dc9.
"""
import pytest
from flose.solutions.floseup_9_card_id_floseup_9_pico_pai_flo_af2dc9 import Floseup9CardIdFloseup9PicoPaiFloAf2dc9Solution

def test_hex_to_hsl_conversion():
    sol = Floseup9CardIdFloseup9PicoPaiFloAf2dc9Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup9CardIdFloseup9PicoPaiFloAf2dc9Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
