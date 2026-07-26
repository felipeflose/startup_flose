"""
Pytest unit test suite for Security Sanitizer: felipe_zero_trust_security_shield_b5eaea.
"""
import pytest
from flose.solutions.felipe_zero_trust_security_shield_b5eaea import FelipeZeroTrustSecurityShieldB5eaeaSolution

def test_xss_sanitization():
    sec = FelipeZeroTrustSecurityShieldB5eaeaSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = FelipeZeroTrustSecurityShieldB5eaeaSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
