"""
Pytest unit test suite for HR Onboarding: kan_9809_recrutamento_contrata_o_para_k_9fb03e.
"""
import pytest
from flose.solutions.kan_9809_recrutamento_contrata_o_para_k_9fb03e import Kan9809RecrutamentoContrataOParaK9fb03eSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9809RecrutamentoContrataOParaK9fb03eSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
