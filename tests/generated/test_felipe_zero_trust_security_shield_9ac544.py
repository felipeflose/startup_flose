"""
Pytest unit test suite for Security Sanitizer: felipe_zero_trust_security_shield_9ac544.
"""
import pytest
from flose.solutions.felipe_zero_trust_security_shield_9ac544 import FelipeZeroTrustSecurityShield9ac544Solution

def test_xss_sanitization():
    sec = FelipeZeroTrustSecurityShield9ac544Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = FelipeZeroTrustSecurityShield9ac544Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
