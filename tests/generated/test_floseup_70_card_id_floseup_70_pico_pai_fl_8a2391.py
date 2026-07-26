"""
Pytest unit test suite for UI Solution: floseup_70_card_id_floseup_70_pico_pai_fl_8a2391.
"""
import pytest
from flose.solutions.floseup_70_card_id_floseup_70_pico_pai_fl_8a2391 import Floseup70CardIdFloseup70PicoPaiFl8a2391Solution

def test_hex_to_hsl_conversion():
    sol = Floseup70CardIdFloseup70PicoPaiFl8a2391Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup70CardIdFloseup70PicoPaiFl8a2391Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
