"""
Pytest unit test suite for UI Solution: floseup_33_pico_mestre_stage_1_refactorin_a5cf9b.
"""
import pytest
from flose.solutions.floseup_33_pico_mestre_stage_1_refactorin_a5cf9b import Floseup33PicoMestreStage1RefactorinA5cf9bSolution

def test_hex_to_hsl_conversion():
    sol = Floseup33PicoMestreStage1RefactorinA5cf9bSolution()
    h, s, l = sol.hex_to_hsl("#3b82f6")
    assert 210 <= h <= 220
    assert s > 80.0

def test_responsive_grid_calculation():
    sol = Floseup33PicoMestreStage1RefactorinA5cf9bSolution()
    grid = sol.calculate_responsive_grid(1920, 1080)
    assert grid["columns"] > 0
    assert grid["rows"] > 0
