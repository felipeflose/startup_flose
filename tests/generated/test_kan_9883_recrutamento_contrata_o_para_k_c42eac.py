"""
Pytest unit test suite for HR Onboarding: kan_9883_recrutamento_contrata_o_para_k_c42eac.
"""
import pytest
from flose.solutions.kan_9883_recrutamento_contrata_o_para_k_c42eac import Kan9883RecrutamentoContrataOParaKC42eacSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9883RecrutamentoContrataOParaKC42eacSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
