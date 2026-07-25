"""
Pytest unit test suite for HR Onboarding: kan_9704_recrutamento_contrata_o_para_k_82fddc.
"""
import pytest
from flose.solutions.kan_9704_recrutamento_contrata_o_para_k_82fddc import Kan9704RecrutamentoContrataOParaK82fddcSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9704RecrutamentoContrataOParaK82fddcSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
