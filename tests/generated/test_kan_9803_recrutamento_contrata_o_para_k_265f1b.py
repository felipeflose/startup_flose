"""
Pytest unit test suite for UI Solution: kan_9803_recrutamento_contrata_o_para_k_265f1b.
"""
import pytest
from flose.solutions.kan_9803_recrutamento_contrata_o_para_k_265f1b import Kan9803RecrutamentoContrataOParaK265f1bSolution

def test_hex_to_hsl_conversion():
    sol = Kan9803RecrutamentoContrataOParaK265f1bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9803RecrutamentoContrataOParaK265f1bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
