"""
Pytest unit test suite for Security Sanitizer: kan_9745_recrutamento_contrata_o_para_k_2f3db5.
"""
import pytest
from flose.solutions.kan_9745_recrutamento_contrata_o_para_k_2f3db5 import Kan9745RecrutamentoContrataOParaK2f3db5Solution

def test_xss_sanitization():
    sec = Kan9745RecrutamentoContrataOParaK2f3db5Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9745RecrutamentoContrataOParaK2f3db5Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
