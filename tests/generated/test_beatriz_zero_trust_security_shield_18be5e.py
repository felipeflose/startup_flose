"""
Pytest unit test suite for Security Sanitizer: beatriz_zero_trust_security_shield_18be5e.
"""
import pytest
from flose.solutions.beatriz_zero_trust_security_shield_18be5e import BeatrizZeroTrustSecurityShield18be5eSolution

def test_xss_sanitization():
    sec = BeatrizZeroTrustSecurityShield18be5eSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = BeatrizZeroTrustSecurityShield18be5eSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
