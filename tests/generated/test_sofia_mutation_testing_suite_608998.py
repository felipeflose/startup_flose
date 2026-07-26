"""
Pytest unit test suite for UI Solution: sofia_mutation_testing_suite_608998.
"""
import pytest
from flose.solutions.sofia_mutation_testing_suite_608998 import SofiaMutationTestingSuite608998Solution

def test_hex_to_hsl_conversion():
    sol = SofiaMutationTestingSuite608998Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaMutationTestingSuite608998Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
