"""
Pytest unit test suite for UI Solution: beatriz_mutation_testing_suite_0bb0d9.
"""
import pytest
from flose.solutions.beatriz_mutation_testing_suite_0bb0d9 import BeatrizMutationTestingSuite0bb0d9Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizMutationTestingSuite0bb0d9Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizMutationTestingSuite0bb0d9Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
