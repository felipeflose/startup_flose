"""
Pytest unit test suite for UI Solution: floseup_14_card_id_floseup_14_branch_feat_e0e768.
"""
import pytest
from flose.solutions.floseup_14_card_id_floseup_14_branch_feat_e0e768 import Floseup14CardIdFloseup14BranchFeatE0e768Solution

def test_hex_to_hsl_conversion():
    sol = Floseup14CardIdFloseup14BranchFeatE0e768Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup14CardIdFloseup14BranchFeatE0e768Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
