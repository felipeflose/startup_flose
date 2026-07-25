"""
Pytest unit test suite for HR Onboarding: kan_9911_recrutamento_contrata_o_para_k_5392cc.
"""
import pytest
from flose.solutions.kan_9911_recrutamento_contrata_o_para_k_5392cc import Kan9911RecrutamentoContrataOParaK5392ccSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9911RecrutamentoContrataOParaK5392ccSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
