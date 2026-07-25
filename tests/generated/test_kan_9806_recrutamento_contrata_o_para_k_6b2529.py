"""
Pytest unit test suite for Security Sanitizer: kan_9806_recrutamento_contrata_o_para_k_6b2529.
"""
import pytest
from flose.solutions.kan_9806_recrutamento_contrata_o_para_k_6b2529 import Kan9806RecrutamentoContrataOParaK6b2529Solution

def test_xss_sanitization():
    sec = Kan9806RecrutamentoContrataOParaK6b2529Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9806RecrutamentoContrataOParaK6b2529Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
