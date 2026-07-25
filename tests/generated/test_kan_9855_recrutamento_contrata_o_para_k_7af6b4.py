"""
Pytest unit test suite for Security Sanitizer: kan_9855_recrutamento_contrata_o_para_k_7af6b4.
"""
import pytest
from flose.solutions.kan_9855_recrutamento_contrata_o_para_k_7af6b4 import Kan9855RecrutamentoContrataOParaK7af6b4Solution

def test_xss_sanitization():
    sec = Kan9855RecrutamentoContrataOParaK7af6b4Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9855RecrutamentoContrataOParaK7af6b4Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
