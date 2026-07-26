"""
Pytest unit test suite for UI Solution: beatriz_mutation_testing_suite_a7957a.
"""
import pytest
from flose.solutions.beatriz_mutation_testing_suite_a7957a import BeatrizMutationTestingSuiteA7957aSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizMutationTestingSuiteA7957aSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizMutationTestingSuiteA7957aSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
