"""
Pytest unit test suite for Security Sanitizer: kan_9711_po_evil_boss_corrigir_sanitiza_410f50.
"""
import pytest
from flose.solutions.kan_9711_po_evil_boss_corrigir_sanitiza_410f50 import Kan9711PoEvilBossCorrigirSanitiza410f50Solution

def test_xss_sanitization():
    sec = Kan9711PoEvilBossCorrigirSanitiza410f50Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9711PoEvilBossCorrigirSanitiza410f50Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
