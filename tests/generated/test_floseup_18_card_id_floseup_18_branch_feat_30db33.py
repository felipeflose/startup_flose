"""
Pytest unit test suite for UI Solution: floseup_18_card_id_floseup_18_branch_feat_30db33.
"""
import pytest
from flose.solutions.floseup_18_card_id_floseup_18_branch_feat_30db33 import Floseup18CardIdFloseup18BranchFeat30db33Solution

def test_hex_to_hsl_conversion():
    sol = Floseup18CardIdFloseup18BranchFeat30db33Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup18CardIdFloseup18BranchFeat30db33Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
