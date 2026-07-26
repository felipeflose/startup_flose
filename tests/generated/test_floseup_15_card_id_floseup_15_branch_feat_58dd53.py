"""
Pytest unit test suite for UI Solution: floseup_15_card_id_floseup_15_branch_feat_58dd53.
"""
import pytest
from flose.solutions.floseup_15_card_id_floseup_15_branch_feat_58dd53 import Floseup15CardIdFloseup15BranchFeat58dd53Solution

def test_hex_to_hsl_conversion():
    sol = Floseup15CardIdFloseup15BranchFeat58dd53Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup15CardIdFloseup15BranchFeat58dd53Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
