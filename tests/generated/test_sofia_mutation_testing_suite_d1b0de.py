"""
Pytest unit test suite for UI Solution: sofia_mutation_testing_suite_d1b0de.
"""
import pytest
from flose.solutions.sofia_mutation_testing_suite_d1b0de import SofiaMutationTestingSuiteD1b0deSolution

def test_hex_to_hsl_conversion():
    sol = SofiaMutationTestingSuiteD1b0deSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = SofiaMutationTestingSuiteD1b0deSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
