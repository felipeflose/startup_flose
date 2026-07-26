"""
Pytest unit test suite for UI Solution: floseup_7_card_id_floseup_7_branch_featu_7c13b5.
"""
import pytest
from flose.solutions.floseup_7_card_id_floseup_7_branch_featu_7c13b5 import Floseup7CardIdFloseup7BranchFeatu7c13b5Solution

def test_hex_to_hsl_conversion():
    sol = Floseup7CardIdFloseup7BranchFeatu7c13b5Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup7CardIdFloseup7BranchFeatu7c13b5Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
