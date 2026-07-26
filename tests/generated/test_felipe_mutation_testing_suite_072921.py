"""
Pytest unit test suite for UI Solution: felipe_mutation_testing_suite_072921.
"""
import pytest
from flose.solutions.felipe_mutation_testing_suite_072921 import FelipeMutationTestingSuite072921Solution

def test_hex_to_hsl_conversion():
    sol = FelipeMutationTestingSuite072921Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = FelipeMutationTestingSuite072921Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
