"""
Pytest unit test suite for Security Sanitizer: felipe_zero_trust_security_shield_86c69d.
"""
import pytest
from flose.solutions.felipe_zero_trust_security_shield_86c69d import FelipeZeroTrustSecurityShield86c69dSolution

def test_xss_sanitization():
    sec = FelipeZeroTrustSecurityShield86c69dSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = FelipeZeroTrustSecurityShield86c69dSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
