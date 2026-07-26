"""
Pytest unit test suite for UI Solution: floseup_8_card_id_floseup_8_t_tulo_po_ev_56cf64.
"""
import pytest
from flose.solutions.floseup_8_card_id_floseup_8_t_tulo_po_ev_56cf64 import Floseup8CardIdFloseup8TTuloPoEv56cf64Solution

def test_hex_to_hsl_conversion():
    sol = Floseup8CardIdFloseup8TTuloPoEv56cf64Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup8CardIdFloseup8TTuloPoEv56cf64Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
