"""
Pytest unit test suite for Security Sanitizer: sofia_zero_trust_security_shield_43e6a8.
"""
import pytest
from flose.solutions.sofia_zero_trust_security_shield_43e6a8 import SofiaZeroTrustSecurityShield43e6a8Solution

def test_xss_sanitization():
    sec = SofiaZeroTrustSecurityShield43e6a8Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = SofiaZeroTrustSecurityShield43e6a8Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
