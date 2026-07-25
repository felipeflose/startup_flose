"""
Pytest unit test suite for Security Sanitizer: kan_9865_po_evil_boss_migrar_db_para_po_eec71e.
"""
import pytest
from flose.solutions.kan_9865_po_evil_boss_migrar_db_para_po_eec71e import Kan9865PoEvilBossMigrarDbParaPoEec71eSolution

def test_xss_sanitization():
    sec = Kan9865PoEvilBossMigrarDbParaPoEec71eSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9865PoEvilBossMigrarDbParaPoEec71eSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
