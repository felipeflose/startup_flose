"""
Pytest unit test suite for Security Sanitizer: kan_9753_po_evil_boss_sanitiza_o_estrit_ee2b5c.
"""
import pytest
from flose.solutions.kan_9753_po_evil_boss_sanitiza_o_estrit_ee2b5c import Kan9753PoEvilBossSanitizaOEstritEe2b5cSolution

def test_xss_sanitization():
    sec = Kan9753PoEvilBossSanitizaOEstritEe2b5cSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9753PoEvilBossSanitizaOEstritEe2b5cSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
