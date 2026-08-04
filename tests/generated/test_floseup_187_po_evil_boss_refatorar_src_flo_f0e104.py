from flose.solutions.floseup_187_po_evil_boss_refatorar_src_flo_f0e104 import *

def test_po_evil_boss_refatorar_sr():
    """
    Testa se a função po_evil_boss_refatorar_sr implementa corretamente a refatoração
    e se a função refatorada possui a docstring esperada.
    """
    # Executa a função refatorada
    auditor = po_evil_boss_refatorar_sr()

    # Verifica se o método existe
    assert hasattr(auditor, 'add_smell')

    # Verifica se a docstring foi adicionada (Verificação da presença da docstring)
    method = auditor.add_smell
    docstring = inspect.getdoc(method)
    
    # Verifica se a docstring existe e contém as seções esperadas
    assert docstring is not None
    assert "Adiciona uma anotação de \"smell\" (cheiro ruim) ao nó AST" in docstring
    assert "Args:" in docstring
    
    # Teste funcional básico
    test_type = "Error"
    test_node = ast.Name(id='test_node', ctx=ast.Load())
    test_msg = "Estrutura AST detectada com anomalia."
    
    result = auditor.add_smell(test_type, test_node, test_msg)
    
    assert result is True
    print("Teste de funcionalidade e docstring concluído com sucesso.")

if __name__ == '__main__':
    # Execução direta para fins de demonstração do teste
    test_po_evil_boss_refatorar_sr()