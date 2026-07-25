"""
Pytest unit test suite for Security Sanitizer: kan_9734_recrutamento_contrata_o_para_k_15d36c.
"""
import pytest
from flose.solutions.kan_9734_recrutamento_contrata_o_para_k_15d36c import Kan9734RecrutamentoContrataOParaK15d36cSolution

def test_xss_sanitization():
    sec = Kan9734RecrutamentoContrataOParaK15d36cSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9734RecrutamentoContrataOParaK15d36cSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
