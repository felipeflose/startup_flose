"""
Pytest unit test suite for Security Sanitizer: felipe_zero_trust_security_shield_bdd76e.
"""
import pytest
from flose.solutions.felipe_zero_trust_security_shield_bdd76e import FelipeZeroTrustSecurityShieldBdd76eSolution

def test_xss_sanitization():
    sec = FelipeZeroTrustSecurityShieldBdd76eSolution()
    dirty = "<script>alert('xss')</script>"
    clean = sec.sanitize_html_xss(dirty)
    assert "<script>" not in clean
    assert "&lt;" in clean

def test_sql_injection_validation():
    sec = FelipeZeroTrustSecurityShieldBdd76eSolution()
    assert sec.validate_sql_safety("SELECT * FROM users; --") is False
    assert sec.validate_sql_safety("user_email@example.com") is True
