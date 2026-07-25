"""
Pytest unit test suite for UI Solution: kan_9738_recrutamento_contrata_o_para_k_130502.
"""
import pytest
from flose.solutions.kan_9738_recrutamento_contrata_o_para_k_130502 import Kan9738RecrutamentoContrataOParaK130502Solution

def test_hex_to_hsl_conversion():
    sol = Kan9738RecrutamentoContrataOParaK130502Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9738RecrutamentoContrataOParaK130502Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
