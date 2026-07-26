"""
Pytest unit test suite for Security Sanitizer: sofia_zero_trust_security_shield_5fc73d.
"""
import pytest
from flose.solutions.sofia_zero_trust_security_shield_5fc73d import SofiaZeroTrustSecurityShield5fc73dSolution

def test_xss_sanitization():
    sec = SofiaZeroTrustSecurityShield5fc73dSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = SofiaZeroTrustSecurityShield5fc73dSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
