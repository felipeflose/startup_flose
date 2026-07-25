"""
Pytest unit test suite for Security Sanitizer: kan_9733_po_evil_boss_sanitiza_o_estrit_77e721.
"""
import pytest
from flose.solutions.kan_9733_po_evil_boss_sanitiza_o_estrit_77e721 import Kan9733PoEvilBossSanitizaOEstrit77e721Solution

def test_xss_sanitization():
    sec = Kan9733PoEvilBossSanitizaOEstrit77e721Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9733PoEvilBossSanitizaOEstrit77e721Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
