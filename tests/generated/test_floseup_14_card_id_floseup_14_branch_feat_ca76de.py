"""
Pytest unit test suite for UI Solution: floseup_14_card_id_floseup_14_branch_feat_ca76de.
"""
import pytest
from flose.solutions.floseup_14_card_id_floseup_14_branch_feat_ca76de import Floseup14CardIdFloseup14BranchFeatCa76deSolution

def test_hex_to_hsl_conversion():
    sol = Floseup14CardIdFloseup14BranchFeatCa76deSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup14CardIdFloseup14BranchFeatCa76deSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
