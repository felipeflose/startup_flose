"""
Pytest unit test suite for HR Onboarding: kan_9884_recrutamento_contrata_o_para_k_c3eb51.
"""
import pytest
from flose.solutions.kan_9884_recrutamento_contrata_o_para_k_c3eb51 import Kan9884RecrutamentoContrataOParaKC3eb51Solution

def test_candidate_onboarding_pipeline():
    hr = Kan9884RecrutamentoContrataOParaKC3eb51Solution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
