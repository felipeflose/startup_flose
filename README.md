# FLOSE - Agentic Enterprise Operating System (AEOS)

## Visão Geral

O **FLOSE** é uma arquitetura de sistema operacional de empresa autônoma baseada em agentes cognitivos de IA.

## Estrutura do Projeto

```text
src/
└── flose/
    ├── core/        # Modelos Pydantic v2, enums e definições constitucionais
    ├── bus/         # EventBus assíncrono com filas de prioridade
    └── engines/     # Engines de Planejamento (WSJF) e Governança (Anti-Alucinação)
tests/               # Suíte de testes unitários automatizados
```

## Como Executar os Testes

1. Crie o ambiente virtual e instale as dependências:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Execute os testes unitários:
```bash
PYTHONPATH=src .venv/bin/pytest tests/
```
