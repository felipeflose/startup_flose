"""
Pytest unit test suite for Security Sanitizer: kan_9711_po_evil_boss_corrigir_sanitiza_ff39be.
"""
import pytest
from flose.solutions.kan_9711_po_evil_boss_corrigir_sanitiza_ff39be import Kan9711PoEvilBossCorrigirSanitizaFf39beSolution

def test_xss_sanitization():
    sec = Kan9711PoEvilBossCorrigirSanitizaFf39beSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9711PoEvilBossCorrigirSanitizaFf39beSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
