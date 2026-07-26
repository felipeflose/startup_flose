"""
Pytest unit test suite for UI Solution: floseup_35_card_id_floseup_35_t_tulo_pico_0c5045.
"""
import pytest
from flose.solutions.floseup_35_card_id_floseup_35_t_tulo_pico_0c5045 import Floseup35CardIdFloseup35TTuloPico0c5045Solution

def test_hex_to_hsl_conversion():
    sol = Floseup35CardIdFloseup35TTuloPico0c5045Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup35CardIdFloseup35TTuloPico0c5045Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
