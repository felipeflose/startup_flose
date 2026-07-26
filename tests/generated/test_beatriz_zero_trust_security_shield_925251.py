"""
Pytest unit test suite for Security Sanitizer: beatriz_zero_trust_security_shield_925251.
"""
import pytest
from flose.solutions.beatriz_zero_trust_security_shield_925251 import BeatrizZeroTrustSecurityShield925251Solution

def test_xss_sanitization():
    sec = BeatrizZeroTrustSecurityShield925251Solution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = BeatrizZeroTrustSecurityShield925251Solution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
