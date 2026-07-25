"""
Pytest unit test suite for UI Solution: kan_9738_recrutamento_contrata_o_para_k_d51f3f.
"""
import pytest
from flose.solutions.kan_9738_recrutamento_contrata_o_para_k_d51f3f import Kan9738RecrutamentoContrataOParaKD51f3fSolution

def test_hex_to_hsl_conversion():
    sol = Kan9738RecrutamentoContrataOParaKD51f3fSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9738RecrutamentoContrataOParaKD51f3fSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
