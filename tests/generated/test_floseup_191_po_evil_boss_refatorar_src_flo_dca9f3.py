# tests/test_gemma_local.py

from flose.solutions.floseup_191_po_evil_boss_refatorar_src_flo_dca9f3 import process_data

def test_process_data():
    input_data = {
        "name": "example",
        "age": 25,
        "city": "new york"
    }
    expected_output = {
        "NAME": "EXAMPLE",
        "AGE": 25,
        "CITY": "NEW YORK"
    }
    assert process_data(input_data) == expected_output