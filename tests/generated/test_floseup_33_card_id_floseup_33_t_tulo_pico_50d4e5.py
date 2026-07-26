"""
Pytest unit test suite for UI Solution: floseup_33_card_id_floseup_33_t_tulo_pico_50d4e5.
"""
import pytest
from flose.solutions.floseup_33_card_id_floseup_33_t_tulo_pico_50d4e5 import Floseup33CardIdFloseup33TTuloPico50d4e5Solution

def test_hex_to_hsl_conversion():
    sol = Floseup33CardIdFloseup33TTuloPico50d4e5Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup33CardIdFloseup33TTuloPico50d4e5Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
