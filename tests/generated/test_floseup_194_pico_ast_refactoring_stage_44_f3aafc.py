# test_flose/solutions/test_floseup_194_pico_ast_refactoring_stage_44_f3aafc.py

from flose.solutions.floseup_194_pico_ast_refactoring_stage_44_f3aafc import *

import pytest

def test_refactor():
    solution = Solution()
    assert solution.refactor('This is an old_string') == 'This is a new_string'
