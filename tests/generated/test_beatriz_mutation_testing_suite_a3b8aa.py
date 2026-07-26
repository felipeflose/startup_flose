"""
Pytest unit test suite for UI Solution: beatriz_mutation_testing_suite_a3b8aa.
"""
import pytest
from flose.solutions.beatriz_mutation_testing_suite_a3b8aa import BeatrizMutationTestingSuiteA3b8aaSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizMutationTestingSuiteA3b8aaSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizMutationTestingSuiteA3b8aaSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
