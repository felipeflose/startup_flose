"""
Pytest unit test suite for Security Sanitizer: felipe_zero_trust_security_shield_e36110.
"""
import pytest
from flose.solutions.felipe_zero_trust_security_shield_e36110 import FelipeZeroTrustSecurityShieldE36110Solution

def test_xss_sanitization():
    sec = FelipeZeroTrustSecurityShieldE36110Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = FelipeZeroTrustSecurityShieldE36110Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
