"""
Pytest unit test suite for HR Onboarding: kan_9751_recrutamento_contrata_o_para_k_a9480d.
"""
import pytest
from flose.solutions.kan_9751_recrutamento_contrata_o_para_k_a9480d import Kan9751RecrutamentoContrataOParaKA9480dSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9751RecrutamentoContrataOParaKA9480dSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
