"""
Pytest unit test suite for UI Solution: floseup_13_card_id_floseup_13_branch_feat_860c60.
"""
import pytest
from flose.solutions.floseup_13_card_id_floseup_13_branch_feat_860c60 import Floseup13CardIdFloseup13BranchFeat860c60Solution

def test_hex_to_hsl_conversion():
    sol = Floseup13CardIdFloseup13BranchFeat860c60Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup13CardIdFloseup13BranchFeat860c60Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
