"""
Pytest unit test suite for UI Solution: floseup_122_card_id_floseup_122_pico_pai_f_e0c194.
"""
import pytest
from flose.solutions.floseup_122_card_id_floseup_122_pico_pai_f_e0c194 import Floseup122CardIdFloseup122PicoPaiFE0c194Solution

def test_hex_to_hsl_conversion():
    sol = Floseup122CardIdFloseup122PicoPaiFE0c194Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup122CardIdFloseup122PicoPaiFE0c194Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
