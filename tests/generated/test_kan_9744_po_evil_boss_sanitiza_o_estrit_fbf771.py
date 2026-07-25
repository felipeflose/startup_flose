"""
Pytest unit test suite for Security Sanitizer: kan_9744_po_evil_boss_sanitiza_o_estrit_fbf771.
"""
import pytest
from flose.solutions.kan_9744_po_evil_boss_sanitiza_o_estrit_fbf771 import Kan9744PoEvilBossSanitizaOEstritFbf771Solution

def test_xss_sanitization():
    sec = Kan9744PoEvilBossSanitizaOEstritFbf771Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9744PoEvilBossSanitizaOEstritFbf771Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
