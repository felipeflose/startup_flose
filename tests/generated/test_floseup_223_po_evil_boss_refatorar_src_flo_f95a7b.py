"""
Testes rigorosos para verificar o comportamento da função de refatoração das docstrings das funções assíncronas.

Este conjunto de testes cobre várias cenários reais para garantir que a refatoração funcione corretamente.
"""

import pytest
from flose.solutions.floseup_223_po_evil_boss_refatorar_src_flo_f95a7b import refactor_async_function_docs

# Cenário 1: Função assíncrona sem docstring
async def test_async_no_docstring():
    node = ast.AsyncFunctionDef(
        name='test_async_no_docstring',
        body=[],
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None),
        decorator_list=[]
    )
    refactor_async_function_docs(node)
    assert node.body[0].value.s == "This is an async function without a docstring."

# Cenário 2: Função assíncrona com uma única linha de docstring
async def test_async_single_line_docstring():
    node = ast.AsyncFunctionDef(
        name='test_async_single_line_docstring',
        body=[],
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None),
        decorator_list=[],
        docstring="A single line docstring"
    )
    refactor_async_function_docs(node)
    assert node.body[0].value.s == "This is an async function with a single line docstring."

# Cenário 3: Função assíncrona com uma docstring em múltiplas linhas
async def test_async_multiline_docstring():
    node = ast.AsyncFunctionDef(
        name='test_async_multiline_docstring',
        body=[],
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None),
        decorator_list=[],
        docstring="This is an async function with a\nmultiline docstring."
    )
    refactor_async_function_docs(node)
    assert node.body[0].value.s == "This is an async function with a multiline docstring."

# Cenário 4: Função assíncrona com uma docstring mal formatada
async def test_async_mal_formatted_docstring():
    node = ast.AsyncFunctionDef(
        name='test_async_mal_formatted_docstring',
        body=[],
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None),
        decorator_list=[],
        docstring="This is a mal formatted docstring"
    )
    refactor_async_function_docs(node)
    assert node.body[0].value.s == "This is an async function with a malformed docstring."

# Cenário 5: Função assíncrona com uma docstring que não atende aos requisitos PEP 257
async def test_async_non_compliant_docstring():
    node = ast.AsyncFunctionDef(
        name='test_async_non_compliant_docstring',
        body=[],
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None),
        decorator_list=[],
        docstring="This is a non-compliant docstring."
    )
    refactor_async_function_docs(node)
    assert node.body[0].value.s == "This is an async function with a non-compliant docstring."