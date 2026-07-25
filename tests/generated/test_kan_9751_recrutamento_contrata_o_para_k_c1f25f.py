"""
Pytest unit test suite for HR Onboarding: kan_9751_recrutamento_contrata_o_para_k_c1f25f.
"""
import pytest
from flose.solutions.kan_9751_recrutamento_contrata_o_para_k_c1f25f import Kan9751RecrutamentoContrataOParaKC1f25fSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9751RecrutamentoContrataOParaKC1f25fSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
