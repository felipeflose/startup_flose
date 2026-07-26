"""
Pytest unit test suite for UI Solution: floseup_115_card_id_floseup_115_pico_pai_f_7e6225.
"""
import pytest
from flose.solutions.floseup_115_card_id_floseup_115_pico_pai_f_7e6225 import Floseup115CardIdFloseup115PicoPaiF7e6225Solution

def test_hex_to_hsl_conversion():
    sol = Floseup115CardIdFloseup115PicoPaiF7e6225Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup115CardIdFloseup115PicoPaiF7e6225Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
