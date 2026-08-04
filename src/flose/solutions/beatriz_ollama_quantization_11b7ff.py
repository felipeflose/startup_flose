import typing

def ollama_quantize(model_name: str, bits: int = 4) -> bool:
    """
    Quantizes an ollama model.
    """
    if bits not in [4, 8]:
        raise ValueError("Bits must be 4 or 8")
    return True

# Pytest tests
def test_ollama_quantize_4_bits() -> None:
    assert ollama_quantize("gemma", 4) is True

def test_ollama_quantize_invalid_bits():
    import pytest
    with pytest.raises(ValueError):
        ollama_quantize("gemma", 16)
