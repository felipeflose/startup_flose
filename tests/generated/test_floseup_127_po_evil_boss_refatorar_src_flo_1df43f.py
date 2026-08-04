from flose.solutions.floseup_127_po_evil_boss_refatorar_src_flo_1df43f import *

def test_po_evil_boss_refatorar_sr():
    # Teste de caso padrão
    result = po_evil_boss_refatorar_sr(project_key="TESTPROJ", epic_name="Test Epic")
    assert result is not None
    assert result.startswith("EPIC-")
    assert result.startswith("TESTPROJ")

    # Teste de caso com valores padrão (verificação de que a lógica base é ativada)
    result_default = po_evil_boss_refatorar_sr()
    assert result_default is not None
    assert result_default.startswith("EPIC-")

    # Teste de caso onde os inputs são vazios (deve retornar None, conforme a refatoração de segurança)
    result_empty = po_evil_boss_refatorar_sr(project_key="", epic_name="Some Epic")
    assert result_empty is None
    
    result_name_empty = po_evil_boss_refatorar_sr(project_key="PROJ1", epic_name="")
    assert result_name_empty is None