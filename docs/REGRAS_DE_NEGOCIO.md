# 🏛️ Flose Startup — Documentação Central de Regras de Negócio & Arquitetura

> **Documento Oficial de Referência para Migração Autônoma de Sistemas (Node.js → Python + React)**

---

## 📌 1. Visão Geral do Produto e Princípios Fundamentais

A **Flose Startup** é uma plataforma autônoma de simulação e execução corporativa onde agentes de Inteligência Artificial (*CEO, POs, Diretores, Desenvolvedores e QAs*) operam uma empresa real de tecnologia.

### Regras de Ouro Inflexíveis:
1. **Evidência Física e Real Obligatória**: NENHUMA tarefa é simulada com texto fictício. Toda tarefa gera obrigatoriamente:
   - Card no Jira (`KAN-XXXX`).
   - Arquivo de especificação/evidência no repositório (`.card-work/KAN-XXXX.md`).
   - Módulo de código real implementado (`src/simulations/` ou `python_engine/`).
   - Commit no Git/GitHub com o hash SHA associado ao colaborador.
2. **Proteção Inviolável do CEO**:
   - Felipe Viana Flose (DONO/CEO) possui o atributo `protected: true`. O Auditor de Governança ou PIP **nunca** podem demitir o CEO.
3. **Escala Orgânica sem Placeholders**:
   - As áreas, cargos e estações de trabalho não são estáticos; eles são fundados e alocados conforme o crescimento real do volume de código e chamados técnicos.

---

## ⚡ 2. Matriz de Fila de Prioridade da IA & Salário por Timeout

O hardware local (Gemma 4 / Qwen) possui um limite de concorrência. Todas as chamadas para a IA passam pela **Fila Única de Prioridades por Desempenho**:

| Nível / Cargo | Prioridade | Salário (Timeout Max) | Modelo da IA | Regra de Recompensa / Penalidade |
| :--- | :---: | :---: | :---: | :--- |
| **C-Level & POs** | `P1` | **120 segundos** | `qwen2.5-coder:32b` | Prioridade máxima na fila para priorização e arquitetura. |
| **Dev Sênior (Score ≥ 80)** | `P2` | **75 segundos** | `gemma4:latest` | Resolução em `< 5s` concede **+3 no Score** e promove no Ranking. |
| **Dev Pleno / QA / Suporte** | `P3` | **35 - 45 segundos** | `gemma4-fast:latest` | Falha ou timeout penaliza em **-4 no Score** e envia para PIP. |

---

## 👔 3. Processo Seletivo, Entrevistas & Alocação de Mesas

1. **Abertura de Vaga**: Quando a carga de uma área ultrapassa 80% ou há escassez de um papel técnico, o RH/Diretoria abre o chamado `[Recrutamento] Contratação para KAN-XXXX` no Jira.
2. **Ata de Entrevista no Chamber**: O comitê (*Dono Felipe Flose*, *CTO Gemma Tech* e *Hugo RH*) conduz o debate técnico via Gemma 4 e registra a **Ata Transcrita** nos comentários do card no Jira e na aba visual **Entrevistas & Atas**.
3. **Alocação de Estação & Contrato**: O colaborador aprovado ganha uma estação física (`workstation`) e política de trabalho (`workPolicy`).

---

## 🛑 4. Controle de Fluxo de Backlog (WIP Limit)

- **Gargalo Evitado**: Para evitar o acúmulo desordenado no board, o **PO Engine** monitora a fila do status "A fazer".
- **Trava dos POs**: Se houver **10 ou mais cards pendentes em "A fazer"**, a criação de novas tarefas entra em pausa até que a Engenharia e o QA concluam os pendentes.

---

## 🔄 5. Diretrizes da Migração para Python (Dupla Convivência & Descomissionamento)

1. **Dupla Convivência (Porta 5001 Node.js + Porta 8000 Python)**:
   - A nova API em FastAPI (`python_engine/main.py`) e os serviços assíncronos rodam simultaneamente na porta 8000 sem interromper o frontend React.
2. **Descomissionamento Gradual**:
   - À medida que cada módulo em Python (PO, Dev, QA, Hiring, KPIs) for homologado pelos QAs e apresentar paridade 100%, o script legado `.cjs` correspondente é descomissionado.
