"""
Pytest unit test suite for UI Solution: floseup_11_card_id_floseup_11_t_tulo_po_e_c47ca0.
"""
import pytest
from flose.solutions.floseup_11_card_id_floseup_11_t_tulo_po_e_c47ca0 import Floseup11CardIdFloseup11TTuloPoEC47ca0Solution

def test_hex_to_hsl_conversion():
    sol = Floseup11CardIdFloseup11TTuloPoEC47ca0Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup11CardIdFloseup11TTuloPoEC47ca0Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
