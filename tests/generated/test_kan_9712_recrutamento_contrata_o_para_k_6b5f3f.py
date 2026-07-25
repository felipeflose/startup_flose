"""
Pytest unit test suite for Security Sanitizer: kan_9712_recrutamento_contrata_o_para_k_6b5f3f.
"""
import pytest
from flose.solutions.kan_9712_recrutamento_contrata_o_para_k_6b5f3f import Kan9712RecrutamentoContrataOParaK6b5f3fSolution

def test_xss_sanitization():
    sec = Kan9712RecrutamentoContrataOParaK6b5f3fSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9712RecrutamentoContrataOParaK6b5f3fSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
