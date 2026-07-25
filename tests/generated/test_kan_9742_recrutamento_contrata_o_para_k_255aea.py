"""
Pytest unit test suite for HR Onboarding: kan_9742_recrutamento_contrata_o_para_k_255aea.
"""
import pytest
from flose.solutions.kan_9742_recrutamento_contrata_o_para_k_255aea import Kan9742RecrutamentoContrataOParaK255aeaSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9742RecrutamentoContrataOParaK255aeaSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
