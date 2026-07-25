"""
Pytest unit test suite for Security Sanitizer: kan_9840_sanitiza_o_estrita_contra_vuln_c7f0ff.
"""
import pytest
from flose.solutions.kan_9840_sanitiza_o_estrita_contra_vuln_c7f0ff import Kan9840SanitizaOEstritaContraVulnC7f0ffSolution

def test_xss_sanitization():
    sec = Kan9840SanitizaOEstritaContraVulnC7f0ffSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = Kan9840SanitizaOEstritaContraVulnC7f0ffSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
