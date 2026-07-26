"""
Pytest unit test suite for UI Solution: floseup_64_card_id_floseup_64_pico_pai_fl_3c3ff6.
"""
import pytest
from flose.solutions.floseup_64_card_id_floseup_64_pico_pai_fl_3c3ff6 import Floseup64CardIdFloseup64PicoPaiFl3c3ff6Solution

def test_hex_to_hsl_conversion():
    sol = Floseup64CardIdFloseup64PicoPaiFl3c3ff6Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup64CardIdFloseup64PicoPaiFl3c3ff6Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
