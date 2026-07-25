"""
Pytest unit test suite for UI Solution: kan_9850_recrutamento_contrata_o_para_k_5b0557.
"""
import pytest
from flose.solutions.kan_9850_recrutamento_contrata_o_para_k_5b0557 import Kan9850RecrutamentoContrataOParaK5b0557Solution

def test_hex_to_hsl_conversion():
    sol = Kan9850RecrutamentoContrataOParaK5b0557Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9850RecrutamentoContrataOParaK5b0557Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
