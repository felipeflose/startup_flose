"""
Pytest unit test suite for Security Sanitizer: beatriz_zero_trust_security_shield_fbebd8.
"""
import pytest
from flose.solutions.beatriz_zero_trust_security_shield_fbebd8 import BeatrizZeroTrustSecurityShieldFbebd8Solution

def test_xss_sanitization():
    sec = BeatrizZeroTrustSecurityShieldFbebd8Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = BeatrizZeroTrustSecurityShieldFbebd8Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
