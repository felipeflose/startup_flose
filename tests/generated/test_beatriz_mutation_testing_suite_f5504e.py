"""
Pytest unit test suite for UI Solution: beatriz_mutation_testing_suite_f5504e.
"""
import pytest
from flose.solutions.beatriz_mutation_testing_suite_f5504e import BeatrizMutationTestingSuiteF5504eSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizMutationTestingSuiteF5504eSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizMutationTestingSuiteF5504eSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
