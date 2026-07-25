"""
Pytest unit test suite for Security Sanitizer: beatriz_zero_trust_security_shield_73c9dd.
"""
import pytest
from flose.solutions.beatriz_zero_trust_security_shield_73c9dd import BeatrizZeroTrustSecurityShield73c9ddSolution

def test_xss_sanitization():
    sec = BeatrizZeroTrustSecurityShield73c9ddSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = BeatrizZeroTrustSecurityShield73c9ddSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
