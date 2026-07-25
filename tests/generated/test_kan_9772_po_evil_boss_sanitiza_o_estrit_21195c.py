"""
Pytest unit test suite for Security Sanitizer: kan_9772_po_evil_boss_sanitiza_o_estrit_21195c.
"""
import pytest
from flose.solutions.kan_9772_po_evil_boss_sanitiza_o_estrit_21195c import Kan9772PoEvilBossSanitizaOEstrit21195cSolution

def test_xss_sanitization():
    sec = Kan9772PoEvilBossSanitizaOEstrit21195cSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9772PoEvilBossSanitizaOEstrit21195cSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
