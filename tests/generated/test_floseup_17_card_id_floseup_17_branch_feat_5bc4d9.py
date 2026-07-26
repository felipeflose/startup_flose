"""
Pytest unit test suite for UI Solution: floseup_17_card_id_floseup_17_branch_feat_5bc4d9.
"""
import pytest
from flose.solutions.floseup_17_card_id_floseup_17_branch_feat_5bc4d9 import Floseup17CardIdFloseup17BranchFeat5bc4d9Solution

def test_hex_to_hsl_conversion():
    sol = Floseup17CardIdFloseup17BranchFeat5bc4d9Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup17CardIdFloseup17BranchFeat5bc4d9Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
