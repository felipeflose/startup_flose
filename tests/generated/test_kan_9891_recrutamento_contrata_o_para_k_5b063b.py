"""
Pytest unit test suite for HR Onboarding: kan_9891_recrutamento_contrata_o_para_k_5b063b.
"""
import pytest
from flose.solutions.kan_9891_recrutamento_contrata_o_para_k_5b063b import Kan9891RecrutamentoContrataOParaK5b063bSolution

def test_candidate_onboarding_pipeline():
    hr = Kan9891RecrutamentoContrataOParaK5b063bSolution()
    rec = hr.process_candidate_onboarding("Gabriel Augusto Silva", "Senior Frontend Dev")
    assert rec["status"] == "ACTIVE_ONBOARDED"
    assert "GitHub" in rec["access_granted"]
    assert hr.verify_compliance(rec) is True
