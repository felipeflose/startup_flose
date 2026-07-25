"""
Pytest unit test suite for Security Sanitizer: kan_9712_recrutamento_contrata_o_para_k_6249bf.
"""
import pytest
from flose.solutions.kan_9712_recrutamento_contrata_o_para_k_6249bf import Kan9712RecrutamentoContrataOParaK6249bfSolution

def test_xss_sanitization():
    sec = Kan9712RecrutamentoContrataOParaK6249bfSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9712RecrutamentoContrataOParaK6249bfSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
