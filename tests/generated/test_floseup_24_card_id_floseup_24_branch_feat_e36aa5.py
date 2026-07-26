"""
Pytest unit test suite for UI Solution: floseup_24_card_id_floseup_24_branch_feat_e36aa5.
"""
import pytest
from flose.solutions.floseup_24_card_id_floseup_24_branch_feat_e36aa5 import Floseup24CardIdFloseup24BranchFeatE36aa5Solution

def test_hex_to_hsl_conversion():
    sol = Floseup24CardIdFloseup24BranchFeatE36aa5Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup24CardIdFloseup24BranchFeatE36aa5Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
