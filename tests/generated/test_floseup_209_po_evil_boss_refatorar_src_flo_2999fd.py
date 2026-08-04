from flose.solutions.floseup_209_po_evil_boss_refatorar_src_flo_2999fd import *

def test_po_evil_boss_refatorar_sr():
    # Test the refactoring function
    result = po_evil_boss_refatorar_sr()
    
    # Assertions to ensure the structure and content are correct
    assert isinstance(result, str)
    
    # Check if the generated CSS contains the expected properties
    expected_css_start = ".po-evil-boss-style {"
    assert expected_css_start in result
    
    # Check for specific extracted properties
    assert "font-size:0.52rem;" in result
    assert "color:${phaseColor};" in result
    assert "font-weight:bold;" in result
    assert "margin-bottom:0.25rem;" in result
    assert "text-align:center;" in result
    
    print("Refactoring test passed successfully.")