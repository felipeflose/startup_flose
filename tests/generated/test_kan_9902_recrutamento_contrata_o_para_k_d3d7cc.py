"""
Pytest unit test suite for HR Onboarding: kan_9902_recrutamento_contrata_o_para_k_d3d7cc.
"""
import pytest
from flose.solutions.kan_9902_recrutamento_contrata_o_para_k_d3d7cc import Kan9902RecrutamentoContrataOParaKD3d7ccSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9902RecrutamentoContrataOParaKD3d7ccSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
