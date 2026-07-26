"""
Pytest unit test suite for UI Solution: beatriz_mutation_testing_suite_9db94b.
"""
import pytest
from flose.solutions.beatriz_mutation_testing_suite_9db94b import BeatrizMutationTestingSuite9db94bSolution

def test_hex_to_hsl_conversion():
    sol = BeatrizMutationTestingSuite9db94bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = BeatrizMutationTestingSuite9db94bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
