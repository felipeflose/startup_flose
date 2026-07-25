"""
Pytest unit test suite for HR Onboarding: kan_9827_recrutamento_contrata_o_para_k_08cdfd.
"""
import pytest
from flose.solutions.kan_9827_recrutamento_contrata_o_para_k_08cdfd import Kan9827RecrutamentoContrataOParaK08cdfdSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9827RecrutamentoContrataOParaK08cdfdSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
