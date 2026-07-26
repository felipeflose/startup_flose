"""
Pytest unit test suite for UI Solution: floseup_12_card_id_floseup_12_branch_feat_1ce4c0.
"""
import pytest
from flose.solutions.floseup_12_card_id_floseup_12_branch_feat_1ce4c0 import Floseup12CardIdFloseup12BranchFeat1ce4c0Solution

def test_hex_to_hsl_conversion():
    sol = Floseup12CardIdFloseup12BranchFeat1ce4c0Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup12CardIdFloseup12BranchFeat1ce4c0Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
