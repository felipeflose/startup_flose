"""
Pytest unit test suite for UI Solution: floseup_43_card_id_floseup_43_pico_pai_fl_0f6913.
"""
import pytest
from flose.solutions.floseup_43_card_id_floseup_43_pico_pai_fl_0f6913 import Floseup43CardIdFloseup43PicoPaiFl0f6913Solution

def test_hex_to_hsl_conversion():
    sol = Floseup43CardIdFloseup43PicoPaiFl0f6913Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup43CardIdFloseup43PicoPaiFl0f6913Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
