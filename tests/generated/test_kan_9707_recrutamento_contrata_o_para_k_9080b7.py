"""
Pytest unit test suite for UI Solution: kan_9707_recrutamento_contrata_o_para_k_9080b7.
"""
import pytest
from flose.solutions.kan_9707_recrutamento_contrata_o_para_k_9080b7 import Kan9707RecrutamentoContrataOParaK9080b7Solution

def test_hex_to_hsl_conversion():
    sol = Kan9707RecrutamentoContrataOParaK9080b7Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Kan9707RecrutamentoContrataOParaK9080b7Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
