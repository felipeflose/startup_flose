"""
Pytest unit test suite for HR Onboarding: kan_9902_recrutamento_contrata_o_para_k_6ec50d.
"""
import pytest
from flose.solutions.kan_9902_recrutamento_contrata_o_para_k_6ec50d import Kan9902RecrutamentoContrataOParaK6ec50dSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9902RecrutamentoContrataOParaK6ec50dSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
