"""
Pytest unit test suite for Security Sanitizer: kan_9734_recrutamento_contrata_o_para_k_722a8d.
"""
import pytest
from flose.solutions.kan_9734_recrutamento_contrata_o_para_k_722a8d import Kan9734RecrutamentoContrataOParaK722a8dSolution

def test_xss_sanitization():
    sec = Kan9734RecrutamentoContrataOParaK722a8dSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9734RecrutamentoContrataOParaK722a8dSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
