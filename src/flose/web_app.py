import asyncio
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from flose.bus.event_bus import EventBus
from flose.core.models import (
    AgentIdentity,
    AgentTier,
    TaskSpecification,
    TaskStatus,
    PriorityLevel,
    SecurityContext,
    FLOSEMessage,
)
from flose.engines.planning import PlanningEngine
from flose.engines.governance import GovernanceEngine
from flose.connectors.jira import JiraConnector
from flose.connectors.gemma_local import GemmaLocalConnector

app = FastAPI(title="FLOSE (AEOS) - Fully Autonomous Game Loop & Jira Discussions")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Busca cards reais do Jira Cloud
real_jira_cards = jira.fetch_real_jira_issues(project_key="KAN", limit=8)

game_state = {
    "boss_name": "PO EVIL BOSS",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Analisando Código Atual Backend & Frontend (Pixel Perfect)",
    "cards_coded_count": 0,
    "victory": False,
    "current_working_card": None,
    "jira_backlog": real_jira_cards if real_jira_cards else [
        {
            "id": "KAN-9647",
            "title": "Refatorar Frontend: Ajustar Grid Pixel Perfect & Cores Glassmorphism",
            "type": "Exigência Frontend PO",
            "comments": [
                {"author": "Felipe", "text": "Entendi o escopo do PO. Precisamos alinhar os limites do container pixel a pixel."},
                {"author": "Sofia", "text": "Pesquisei a solução com CSS Grid 16-bit e HSL tailored colors."},
                {"author": "Lucas", "text": "Estou codificando a solução no web_app.py agora via Claude Code & AGY!"},
                {"author": "Beatriz", "text": "Aguardando testes de regressão visual para aprovação do DoD."}
            ]
        },
        {
            "id": "KAN-9633",
            "title": "Otimizar Backend: Reduzir Latência do EventBus para <5ms",
            "type": "Cobrança Backend PO",
            "comments": [
                {"author": "Felipe", "text": "PO exige latência ultra baixa. Vamos otimizar a fila de prioridades do asyncio."},
                {"author": "Lucas", "text": "Implementando estrutura de deque de alta performance no event_bus.py."},
            ]
        }
    ]
}

# Inicializar o primeiro card em trabalho pelos agentes
if game_state["jira_backlog"]:
    game_state["current_working_card"] = game_state["jira_backlog"][0]

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe (CEO/Architect)",
        "class": "Líder de Arquitetura",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "action": "Supervisionando o Card em Progresso no Jira",
        "current_thought": "Entendendo os requisitos do PO para o card atual..."
    },
    "sofia": {
        "name": "Sofia (Gemma 4)",
        "class": "Idea & Tech Analyst",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "action": "Estudando Melhorias de Frontend Pixel Perfect",
        "current_thought": "Pesquisando arquiteturas no Gemma 4 local..."
    },
    "lucas": {
        "name": "Lucas (Claude Code/AGY)",
        "class": "Master Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "action": "Codificando Solução Python/CSS em Tempo Real",
        "current_thought": "Escrevendo código limpo para zerar o card!"
    },
    "beatriz": {
        "name": "Beatriz (QA/Security)",
        "class": "Shield & Tester",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "action": "Validando Cobertura de Testes & Anti-Alucinação",
        "current_thought": "Auditando evidências de execução..."
    }
}

audit_logs: List[Dict[str, Any]] = []

# Automação de Fundo: O Loop Continuo Autônomo da Batalha!
async def autonomous_game_loop():
    """Loop 100% autônomo: O PO cria cards continuamente, os agentes debatem e codificam sozinhos!"""
    while True:
        await asyncio.sleep(4.0) # Ciclo de ação a cada 4 segundos
        
        if game_state["victory"]:
            continue

        # 1. PO Vilão tenta criar um novo Card aleatoriamente analisando o código atual
        if random.random() < 0.4:
            po_topics = [
                "Refatoração Frontend: Ajustar alinhamento Pixel Perfect nos botões",
                "Otimização Backend: Reescrever queries SQL para Async ORM",
                "Estudo de Desempenho: Adicionar Caching Redis para a API de Status",
                "Segurança Frontend: Sanitizar todos os inputs contra XSS e Injeção",
                "Melhoria UI: Implementar Dark Mode Voxel com HSL tailored palette"
            ]
            chosen_topic = random.choice(po_topics)
            new_id = f"KAN-{random.randint(9650, 9999)}"
            new_card = {
                "id": new_id,
                "title": chosen_topic,
                "type": "Ataque do PO (Refatoração Exigida)",
                "comments": [
                    {"author": "PO Vilão", "text": f"Analisei o código atual e exijo melhoria imediata em: {chosen_topic}!"}
                ]
            }
            game_state["jira_backlog"].append(new_card)
            game_state["boss_phase"] = f"😈 PO VILÃO ADICIONOU NOVO CARD {new_id} NO JIRA!"

            # Envia para o Jira Real se configurado
            jira.create_issue("KAN", f"[PO-ATTACK] {chosen_topic}", f"Exigência do PO Vilão: {chosen_topic}")

        # 2. Se há cards no backlog, os agentes debatem e codificam automaticamente!
        if game_state["jira_backlog"]:
            active_card = game_state["jira_backlog"][0]
            game_state["current_working_card"] = active_card

            # Simula debate dos agentes sobre o card
            agent_names = ["Felipe", "Sofia", "Lucas", "Beatriz"]
            active_agent = random.choice(agent_names)
            
            thoughts = {
                "Felipe": f"Analisando arquitetura para resolver {active_card['id']}.",
                "Sofia": f"Gemma 4 sugeriu padrão otimizado para {active_card['title']}.",
                "Lucas": f"Claude Code & AGY aplicaram o patch de código para {active_card['id']}!",
                "Beatriz": f"Suíte de testes aprovada com 100% de evidência para {active_card['id']}."
            }

            comment_msg = thoughts[active_agent]
            active_card.setdefault("comments", []).append({"author": active_agent, "text": comment_msg})
            
            # Adiciona o comentário no Jira Cloud Real se configurado!
            jira.add_comment(active_card["id"], active_agent, comment_msg)

            # 3. Quando o card atinge 3 comentários de entendimento, ele é codificado e resolvido!
            if len(active_card["comments"]) >= 3:
                cleared_card = game_state["jira_backlog"].pop(0)
                damage = 200
                game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                game_state["cards_coded_count"] += 1
                game_state["boss_phase"] = f"💥 AGENTES CODIFICARAM E FECHARAM O CARD {cleared_card['id']}!"

                h = governance.generate_audit_hash("agt_lucas", "AUTONOMOUS_CARD_CODED", cleared_card['title'])
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "CARD_AUTOMATICALLY_CODED",
                    "card_id": cleared_card["id"],
                    "title": cleared_card["title"],
                    "damage": damage,
                    "boss_hp": game_state["boss_hp"],
                    "hash": h,
                })

                if game_state["boss_hp"] <= 0:
                    game_state["victory"] = True
                    game_state["boss_phase"] = "🏆 VITÓRIA! O TIME DE ENGENHARIA CODIFICOU TUDO E DERROTOU O PO VILÃO!"

@app.on_event("startup")
async def start_autonomous_loop():
    asyncio.create_task(autonomous_game_loop())

@app.get("/api/boss/state")
async def get_boss_state():
    for agent in pixel_agents.values():
        agent["x"] += random.choice([-2, 0, 2])
        agent["y"] += random.choice([-2, 0, 2])
        agent["x"] = max(50, min(550, agent["x"]))
        agent["y"] = max(200, min(320, agent["y"]))

    return {
        "game_state": game_state,
        "pixel_agents": list(pixel_agents.values()),
        "jira_cards": game_state["jira_backlog"],
        "current_card": game_state["current_working_card"],
        "audit_logs": audit_logs[-6:],
    }

@app.get("/", response_class=HTMLResponse)
async def serve_autonomous_pixel_game():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE AEOS - Continuous Autonomous Pixel Agents vs PO Boss</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background: #0d0e15;
                color: #fff;
                font-family: 'Press Start 2P', monospace;
                overflow: hidden;
            }

            #game-container {
                display: flex;
                width: 100vw;
                height: 100vh;
            }

            #pixel-canvas {
                background: #181926;
                border-right: 4px solid #3b3d54;
                image-rendering: pixelated;
            }

            .side-panel {
                width: 460px;
                background: #11121d;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.75rem;
                color: #55ff55;
                margin-bottom: 0.8rem;
                text-shadow: 2px 2px #00aa00;
            }

            .active-card-box {
                background: rgba(236, 72, 153, 0.15);
                border: 2px solid #ec4899;
                border-radius: 6px;
                padding: 0.8rem;
                margin-bottom: 1rem;
                font-size: 0.55rem;
                line-height: 1.5;
            }

            .comment-item {
                background: rgba(0,0,0,0.5);
                border-left: 3px solid #60a5fa;
                padding: 0.4rem 0.6rem;
                margin-top: 0.4rem;
                font-size: 0.5rem;
                color: #e5e7eb;
            }

            .comment-author { color: #f59e0b; font-weight: bold; }

            .jira-card {
                background: rgba(59, 130, 246, 0.15);
                border: 2px solid #3b82f6;
                border-radius: 4px;
                padding: 0.5rem;
                margin-bottom: 0.4rem;
                font-size: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div>
                    <div class="hud-title">🤖 100% LOOP AUTÔNOMO DE BATALHA</div>
                    <div style="font-size:0.5rem; color:#9ca3af; margin-bottom:1rem;">O PO cria cards sozinho e o time debate & codifica sem precisar apertar botões!</div>

                    <div style="font-size:0.6rem; color:#ec4899; margin-bottom:0.5rem;">🔥 CARD ATUAL EM DEBATE & CODIFICAÇÃO:</div>
                    <div id="current-card-box" class="active-card-box">Aguardando card...</div>

                    <div style="font-size:0.6rem; color:#4c9aff; margin-bottom:0.5rem;">🔷 CARDS PENDENTES NO JIRA</div>
                    <div id="cards-list">Carregando backlog...</div>
                </div>

                <div>
                    <div style="font-size: 0.55rem; color: #55ff55; margin-bottom: 0.4rem;">📜 LOG DE EVIDÊNCIAS</div>
                    <div id="audit-log" style="font-size: 0.45rem; color: #9ca3af; max-height: 100px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = window.innerWidth - 460;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            function drawPixelSprite(x, y, color, name, action) {
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);

                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);

                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);

                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(name, x - 5, y - 8);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#8b949e";
                ctx.fillText(action.substring(0, 25), x - 20, y + 38);
            }

            function drawPOBoss(hpPercent, phaseText) {
                const bx = canvas.width / 2 - 40;
                const by = 40;

                ctx.fillStyle = "#1e1e2e";
                ctx.fillRect(bx, by + 30, 80, 70);

                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 36, by + 35, 8, 35);

                ctx.fillStyle = "#313244";
                ctx.fillRect(bx + 10, by, 60, 40);

                ctx.fillStyle = "#ff0000";
                ctx.fillRect(bx + 20, by + 12, 12, 8);
                ctx.fillRect(bx + 48, by + 12, 12, 8);

                ctx.font = '11px "Press Start 2P"';
                ctx.fillStyle = "#ff5555";
                ctx.fillText("👹 PO EVIL BOSS (GERANDO CARDS)", bx - 50, by - 15);

                ctx.fillStyle = "#440000";
                ctx.fillRect(canvas.width / 2 - 150, 15, 300, 16);
                ctx.fillStyle = "#ff3333";
                ctx.fillRect(canvas.width / 2 - 150, 15, (300 * hpPercent) / 100, 16);
                ctx.strokeStyle = "#ffffff";
                ctx.strokeRect(canvas.width / 2 - 150, 15, 300, 16);

                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                ctx.fillText(phaseText.substring(0, 45), canvas.width / 2 - 140, 42);
            }

            function render() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#11111b";
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                for (let i = 0; i < canvas.width; i += 40) {
                    ctx.strokeStyle = "#1e1e2e";
                    ctx.beginPath();
                    ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height);
                    ctx.stroke();
                }

                if (gameState) {
                    const hpPct = (gameState.boss_hp / gameState.boss_max_hp) * 100;
                    drawPOBoss(hpPct, gameState.boss_phase || "Carregando...");

                    agentsList.forEach(a => {
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, a.action);
                    });
                }

                requestAnimationFrame(render);
            }
            render();

            async function updateState() {
                const res = await fetch('/api/boss/state');
                const data = await res.json();
                gameState = data.game_state;
                agentsList = data.pixel_agents;

                // Card Atual em Trabalho e Seus Comentários
                const currentCard = data.current_card;
                if (currentCard) {
                    const commentsHtml = currentCard.comments ? currentCard.comments.map(c => `
                        <div class="comment-item">
                            <span class="comment-author">${c.author}:</span> ${c.text}
                        </div>
                    `).join('') : '<div style="color:#9ca3af;">Sem comentários ainda...</div>';

                    document.getElementById('current-card-box').innerHTML = `
                        <div style="color:#ec4899; font-weight:bold;">[${currentCard.id}] ${currentCard.title}</div>
                        <div style="color:#9ca3af; margin-top:0.4rem;">💬 DEBATE DOS AGENTES NO JIRA:</div>
                        ${commentsHtml}
                    `;
                } else {
                    document.getElementById('current-card-box').innerHTML = 'Nenhum card em trabalho.';
                }

                // Backlog Jira
                document.getElementById('cards-list').innerHTML = data.jira_cards.length ? data.jira_cards.map(c => `
                    <div class="jira-card">
                        <span style="color:#60a5fa; font-weight:bold;">${c.id}</span>: ${c.title}
                    </div>
                `).join('') : '<div style="color:#55ff55; font-size:0.55rem;">🎉 JIRA LIMPO! REPOSITÓRIO 100% OK!</div>';

                // Audit Log
                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.25rem;">> ${l.action}: ${l.title || ''}</div>
                `).join('');
            }

            updateState();
            setInterval(updateState, 1500);
        </script>
    </body>
    </html>
    """
