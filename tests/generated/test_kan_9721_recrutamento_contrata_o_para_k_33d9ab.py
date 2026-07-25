"""
Pytest unit test suite for HR Onboarding: kan_9721_recrutamento_contrata_o_para_k_33d9ab.
"""
import pytest
from flose.solutions.kan_9721_recrutamento_contrata_o_para_k_33d9ab import Kan9721RecrutamentoContrataOParaK33d9abSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9721RecrutamentoContrataOParaK33d9abSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
