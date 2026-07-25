"""
Pytest unit test suite for Security Sanitizer: kan_9805_po_evil_boss_sanitiza_o_estrit_d73849.
"""
import pytest
from flose.solutions.kan_9805_po_evil_boss_sanitiza_o_estrit_d73849 import Kan9805PoEvilBossSanitizaOEstritD73849Solution

def test_xss_sanitization():
    sec = Kan9805PoEvilBossSanitizaOEstritD73849Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9805PoEvilBossSanitizaOEstritD73849Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
