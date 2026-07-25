"""
Pytest unit test suite for HR Onboarding: kan_9869_po_evil_boss_refatorar_kan_984_275aef.
"""
import pytest
from flose.solutions.kan_9869_po_evil_boss_refatorar_kan_984_275aef import Kan9869PoEvilBossRefatorarKan984275aefSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9869PoEvilBossRefatorarKan984275aefSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
