"""
Pytest unit test suite for HR Onboarding: kan_9719_recrutamento_contrata_o_para_k_02889f.
"""
import pytest
from flose.solutions.kan_9719_recrutamento_contrata_o_para_k_02889f import Kan9719RecrutamentoContrataOParaK02889fSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9719RecrutamentoContrataOParaK02889fSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
