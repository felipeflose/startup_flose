import pytest
from flose.solutions.floseup_199_po_evil_boss_refatorar_src_flo_bdaf39 import po_evil_boss_refatorar_sr

def test_refactoring_success():
    # Simulating the code snippet from L1349 of web_app.py
    original_code = """
👔 <b>Felipe:</b> Analisou & Delegou para <span style="color:#a855f7;">${duel.active_hero}</span>!
"""
    
    # Execute the refactoring function
    refactored_code = po_evil_boss_refatorar_sr(original_code)
    
    # Define the expected output based on the simulated transformation logic
    expected_refactoring = 'class="style-color-a855f7"'
    
    # Assert that the refactoring successfully identified and attempted to replace the inline style
    assert expected_refactoring in refactored_code
    
    # Verify that the output is structurally different (i.e., the transformation occurred)
    assert original_code != refactored_code