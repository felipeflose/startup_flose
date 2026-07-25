"""
Pytest unit test suite for Security Sanitizer: kan_9733_po_evil_boss_sanitiza_o_estrit_b28ffa.
"""
import pytest
from flose.solutions.kan_9733_po_evil_boss_sanitiza_o_estrit_b28ffa import Kan9733PoEvilBossSanitizaOEstritB28ffaSolution

def test_xss_sanitization():
    sec = Kan9733PoEvilBossSanitizaOEstritB28ffaSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9733PoEvilBossSanitizaOEstritB28ffaSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
