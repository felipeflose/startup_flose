"""
Pytest unit test suite for HR Onboarding: kan_9781_recrutamento_contrata_o_para_k_021e8a.
"""
import pytest
from flose.solutions.kan_9781_recrutamento_contrata_o_para_k_021e8a import Kan9781RecrutamentoContrataOParaK021e8aSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9781RecrutamentoContrataOParaK021e8aSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
