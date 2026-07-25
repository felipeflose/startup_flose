"""
Pytest unit test suite for HR Onboarding: kan_9698_recrutamento_contrata_o_para_k_2a42ac.
"""
import pytest
from flose.solutions.kan_9698_recrutamento_contrata_o_para_k_2a42ac import Kan9698RecrutamentoContrataOParaK2a42acSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9698RecrutamentoContrataOParaK2a42acSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
