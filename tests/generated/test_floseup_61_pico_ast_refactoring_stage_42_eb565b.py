from flose.solutions.floseup_61_pico_ast_refactoring_stage_42_eb565b import refactor_code

def test_refactor_code():
    assert refactor_code('def foo(bar: Type[int]) -> Type[str]:') == 'def foo(bar: int) -> str:'
    assert refactor_code('x: Type[float] = 3.14') == 'x: float = 3.14'
