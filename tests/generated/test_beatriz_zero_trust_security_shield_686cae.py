"""
Pytest unit test suite for Security Sanitizer: beatriz_zero_trust_security_shield_686cae.
"""
import pytest
from flose.solutions.beatriz_zero_trust_security_shield_686cae import BeatrizZeroTrustSecurityShield686caeSolution

def test_xss_sanitization():
    sec = BeatrizZeroTrustSecurityShield686caeSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = BeatrizZeroTrustSecurityShield686caeSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
