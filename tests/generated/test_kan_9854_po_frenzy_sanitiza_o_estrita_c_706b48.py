"""
Pytest unit test suite for Security Sanitizer: kan_9854_po_frenzy_sanitiza_o_estrita_c_706b48.
"""
import pytest
from flose.solutions.kan_9854_po_frenzy_sanitiza_o_estrita_c_706b48 import Kan9854PoFrenzySanitizaOEstritaC706b48Solution

def test_xss_sanitization():
    sec = Kan9854PoFrenzySanitizaOEstritaC706b48Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9854PoFrenzySanitizaOEstritaC706b48Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
