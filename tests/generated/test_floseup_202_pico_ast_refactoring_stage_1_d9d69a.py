from flose.solutions.floseup_202_pico_ast_refactoring_stage_1_d9d69a import *

import ast
import unittest

class TestPicoAstRefactoring(unittest.TestCase):
    def test_pico_ast_refactoring_stag_name(self):
        # Teste para refatorar um nó ast.Name
        original_name = ast.Name(id='variable', ctx=ast.Load())
        refactored_name = pico_ast_refactoring_stag(original_name)
        self.assertEqual(refactored_name.id, 'VARIABLE')

    def test_pico_ast_refactoring_stag_call(self):
        # Teste para refatorar um nó ast.Call
        original_call = ast.Call(func=ast.Name(id='some function', ctx=ast.Load()), args=[ast.Constant(value=1)])
        refactored_call = pico_ast_refactoring_stag(original_call)
        self.assertEqual(refactored_call.func.id, 'SOME_FUNCTION')

if __name__ == '__main__':
    unittest.main()