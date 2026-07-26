"""
Pytest unit test suite for UI Solution: floseup_37_card_id_floseup_37_t_tulo_pico_a63e2b.
"""
import pytest
from flose.solutions.floseup_37_card_id_floseup_37_t_tulo_pico_a63e2b import Floseup37CardIdFloseup37TTuloPicoA63e2bSolution

def test_hex_to_hsl_conversion():
    sol = Floseup37CardIdFloseup37TTuloPicoA63e2bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup37CardIdFloseup37TTuloPicoA63e2bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
