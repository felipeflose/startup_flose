"""
Pytest unit test suite for UI Solution: sofia_mutation_testing_suite_bf0253.
"""
import pytest
from flose.solutions.sofia_mutation_testing_suite_bf0253 import SofiaMutationTestingSuiteBf0253Solution

def test_hex_to_hsl_conversion():
    sol = SofiaMutationTestingSuiteBf0253Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaMutationTestingSuiteBf0253Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
