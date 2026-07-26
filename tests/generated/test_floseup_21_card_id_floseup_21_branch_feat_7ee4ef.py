"""
Pytest unit test suite for UI Solution: floseup_21_card_id_floseup_21_branch_feat_7ee4ef.
"""
import pytest
from flose.solutions.floseup_21_card_id_floseup_21_branch_feat_7ee4ef import Floseup21CardIdFloseup21BranchFeat7ee4efSolution

def test_hex_to_hsl_conversion():
    sol = Floseup21CardIdFloseup21BranchFeat7ee4efSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup21CardIdFloseup21BranchFeat7ee4efSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
