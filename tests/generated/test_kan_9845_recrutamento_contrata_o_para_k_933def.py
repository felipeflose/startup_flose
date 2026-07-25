"""
Pytest unit test suite for UI Solution: kan_9845_recrutamento_contrata_o_para_k_933def.
"""
import pytest
from flose.solutions.kan_9845_recrutamento_contrata_o_para_k_933def import Kan9845RecrutamentoContrataOParaK933defSolution

def test_hex_to_hsl_conversion():
    sol = Kan9845RecrutamentoContrataOParaK933defSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9845RecrutamentoContrataOParaK933defSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
