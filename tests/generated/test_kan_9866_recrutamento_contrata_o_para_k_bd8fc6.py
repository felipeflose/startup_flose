"""
Pytest unit test suite for Security Sanitizer: kan_9866_recrutamento_contrata_o_para_k_bd8fc6.
"""
import pytest
from flose.solutions.kan_9866_recrutamento_contrata_o_para_k_bd8fc6 import Kan9866RecrutamentoContrataOParaKBd8fc6Solution

def test_xss_sanitization():
    sec = Kan9866RecrutamentoContrataOParaKBd8fc6Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9866RecrutamentoContrataOParaKBd8fc6Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
