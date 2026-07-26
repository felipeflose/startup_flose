"""
Pytest unit test suite for UI Solution: beatriz_mutation_testing_suite_8106e4.
"""
import pytest
from flose.solutions.beatriz_mutation_testing_suite_8106e4 import BeatrizMutationTestingSuite8106e4Solution

def test_hex_to_hsl_conversion():
    sol = BeatrizMutationTestingSuite8106e4Solution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizMutationTestingSuite8106e4Solution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
