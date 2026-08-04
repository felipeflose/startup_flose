from flose.solutions.floseup_65_pico_ast_refactoring_stage_42_691bf1 import *

def test_calculate_total():
    items = [{'price': 10, 'quantity': 2}, {'price': 5, 'quantity': 3}]
    assert calculate_total(items) == 40
