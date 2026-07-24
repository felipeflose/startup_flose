import asyncio
import time
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

app = FastAPI(title="FLOSE (AEOS) - Strict PO Validation Lifecycle Game Loop")

bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Regra estrita de Kanban Workflow:
# [1. A Fazer (To Do)] -> [2. Em Progresso] -> [3. Em Validação] -> [4. Validação PO (Aprovado/Barrado)] -> [5. Concluído (Done)]
game_state = {
    "boss_name": "PO EVIL BOSS",
    "boss_hp": 1000,
    "boss_max_hp": 1000,
    "boss_phase": "Auditando Cards 'Em Validação' (Barrando Qualquer Problema)",
    "cards_coded_count": 0,
    "victory": False,
    "current_working_card": None,
    "kanban": {
        "to_do": [],
        "in_progress": [],
        "in_validation": [],
        "done": []
    }
}

pixel_agents: Dict[str, Dict[str, Any]] = {
    "felipe": {
        "name": "Felipe",
        "class": "Líder de Arquitetura & RH",
        "sprite_color": "#3b82f6",
        "x": 100, "y": 260,
        "skill_level": 1,
        "actual_latency_ms": 120.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Supervisionando Mover de Cards para 'Em Validação'",
    },
    "sofia": {
        "name": "Sofia",
        "class": "Gemma 4 Idea Miner",
        "sprite_color": "#ec4899",
        "x": 220, "y": 220,
        "skill_level": 1,
        "actual_latency_ms": 180.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Minerando Requisitos para o Card no 'A Fazer'",
    },
    "lucas": {
        "name": "Lucas",
        "class": "Claude Code Master Coder",
        "sprite_color": "#f97316",
        "x": 350, "y": 270,
        "skill_level": 1,
        "actual_latency_ms": 90.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Codificando e Movendo Card para 'Em Validação'",
    },
    "beatriz": {
        "name": "Beatriz",
        "class": "QA & Security Shield",
        "sprite_color": "#10b981",
        "x": 480, "y": 230,
        "skill_level": 1,
        "actual_latency_ms": 140.0,
        "target_max_ms": 600.0,
        "health_pct": 100.0,
        "action": "Auditando Testes antes da Validação do PO",
    }
}

audit_logs: List[Dict[str, Any]] = []

@app.post("/api/agents/upgrade_skill")
async def upgrade_agent_skill(agent_key: str):
    if agent_key not in pixel_agents:
        raise HTTPException(status_code=404, detail="Agente não encontrado")

    agent = pixel_agents[agent_key]
    agent["skill_level"] += 1
    agent["target_max_ms"] = max(200.0, agent["target_max_ms"] - 50.0)
    agent["actual_latency_ms"] = max(20.0, agent["actual_latency_ms"] * 0.75)
    agent["health_pct"] = 100.0

    return {"message": f"Skill de {agent['name']} aprimorada para Nível {agent['skill_level']}!", "agent": agent}

# LOOP AUTÔNOMO SEGUINDO A REGRA ESTRITA DO PO VILÃO
async def strict_po_lifecycle_game_loop():
    while True:
        await asyncio.sleep(3.5)
        
        if game_state["victory"]:
            continue

        # -------------------------------------------------------------
        # PASSO 1: O PO VILÃO CRIA O CARD NO 'A FAZER' (TO DO) NO JIRA REAL
        # -------------------------------------------------------------
        if random.random() < 0.4 and len(game_state["kanban"]["to_do"]) < 4:
            po_topics = [
                ("Refatoração Frontend Pixel Perfect nos Botões", "PO exige alinhamento perfeito de bordas HSL no CSS."),
                ("Otimizar Queries Backend para <5ms", "PO exige reescrita Async ORM com verificação de latência estrita."),
                ("Corrigir Sanitização de Inputs XSS", "PO encontrou potencial vulnerabilidade na entrada de dados."),
                ("Adicionar Suíte de Testes de Mutação", "PO exige cobertura comprovada de 100% no log imutável.")
            ]
            title, desc = random.choice(po_topics)
            jira_res = jira.create_detailed_epic_or_task("KAN", title, desc, "ÉPICO VILÃO PO")
            new_key = jira_res.get("key", f"KAN-{random.randint(9700, 9999)}")
            
            new_card = {
                "id": new_key,
                "title": title,
                "description": desc,
                "status": "A FAZER",
                "rejections": 0,
                "comments": [{"author": "PO EVIL BOSS", "text": f"Criado no 'A FAZER': {title}. Quero ver se conseguem passar na minha validação!"}]
            }
            game_state["kanban"]["to_do"].append(new_card)
            game_state["boss_phase"] = f"😈 PO VILÃO CRIOU O CARD {new_key} NO 'A FAZER'!"
            
            audit_logs.append({
                "event_id": f"evt_{len(audit_logs)+1}",
                "action": "PO_CREATED_CARD_IN_TO_DO",
                "card_id": new_key,
                "title": title
            })

        # -------------------------------------------------------------
        # PASSO 2: OS AGENTES PEGAM O CARD DO 'A FAZER', AJUSTAM E MOVEM PARA 'EM VALIDAÇÃO'
        # -------------------------------------------------------------
        if game_state["kanban"]["to_do"] and not game_state["kanban"]["in_progress"] and not game_state["kanban"]["in_validation"]:
            card = game_state["kanban"]["to_do"].pop(0)
            card["status"] = "EM PROGRESSO"
            game_state["kanban"]["in_progress"].append(card)
            game_state["current_working_card"] = card
            
            # Agentes atuam e ajustam o código
            t_start = time.perf_counter()
            await asyncio.sleep(0.1)
            t_end = time.perf_counter()
            
            lucas = pixel_agents["lucas"]
            lucas["actual_latency_ms"] = round((t_end - t_start) * 1000.0 + (90.0 / lucas["skill_level"]), 1)
            
            card["comments"].append({"author": "Lucas", "text": f"Ajustei o código para {card['id']}. Movendo para 'EM VALIDAÇÃO'!"})
            jira.add_comment(card["id"], "Lucas", f"Ajuste concluído em {lucas['actual_latency_ms']}ms. Movendo para Em Validação.")

            # Mover para Em Validação
            game_state["kanban"]["in_progress"].remove(card)
            card["status"] = "EM VALIDAÇÃO"
            game_state["kanban"]["in_validation"].append(card)
            game_state["boss_phase"] = f"🛠️ AGENTES MOVERAM O CARD {card['id']} PARA 'EM VALIDAÇÃO'!"

        # -------------------------------------------------------------
        # PASSO 3: O PO VILÃO VÊ O CARD EM 'EM VALIDAÇÃO' E AUDITA (BEM CHATO!)
        # -------------------------------------------------------------
        if game_state["kanban"]["in_validation"]:
            card_val = game_state["kanban"]["in_validation"].pop(0)
            
            # O PO Vilão é super chato! Se a latência de qualquer herói for alta ou tiver poucas habilidades, ele BARRA!
            lucas_lat = pixel_agents["lucas"]["actual_latency_ms"]
            po_rejection_chance = 0.5 if lucas_lat > 120.0 or card_val["rejections"] == 0 else 0.15

            if random.random() < po_rejection_chance:
                # PO BARRA O CARD E MANDAR DE VOLTA PRO 'A FAZER'!
                card_val["rejections"] += 1
                card_val["status"] = "A FAZER"
                card_val["comments"].append({"author": "PO EVIL BOSS", "text": f"❌ CARD BARRADO! Encontrei detalhes no código! Volte para o 'A FAZER' e refaça!"})
                jira.add_comment(card_val["id"], "PO EVIL BOSS", f"CARD BARRADO NA VALIDAÇÃO! Refazer requisitos de qualidade.")
                
                game_state["kanban"]["to_do"].append(card_val)
                game_state["boss_phase"] = f"🚫 PO VILÃO BARROU O CARD {card_val['id']}! VOLTOU PRO 'A FAZER'!"
                
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "PO_REJECTED_CARD",
                    "card_id": card_val["id"],
                    "rejections": card_val["rejections"]
                })
            else:
                # PO APROVA O CARD! CARD VAI PRO 'CONCLUÍDO (DONE)' E CAUSA DANO NO VILÃO!
                card_val["status"] = "CONCLUÍDO"
                card_val["comments"].append({"author": "PO EVIL BOSS", "text": "✅ Incrivelmente o código passou na minha validação rígida. Aprovado!"})
                jira.add_comment(card_val["id"], "PO EVIL BOSS", "Aprovado na Validação Rígida do PO.")

                damage = 250
                game_state["boss_hp"] = max(0, game_state["boss_hp"] - damage)
                game_state["kanban"]["done"].append(card_val)
                game_state["cards_coded_count"] += 1

                # Heróis recuperam vida ao passar na validação do PO!
                for agt in pixel_agents.values():
                    agt["health_pct"] = 100.0

                game_state["boss_phase"] = f"💥 PO VILÃO TEVE QUE APROVAR O CARD {card_val['id']}! (-250 HP)"

                h = governance.generate_audit_hash("agt_lucas", "CARD_APPROVED_BY_STRICT_PO", card_val['title'])
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "PO_APPROVED_CARD_TO_DONE",
                    "card_id": card_val["id"],
                    "damage": damage,
                    "boss_hp": game_state["boss_hp"],
                    "hash": h,
                })

                if game_state["boss_hp"] <= 0:
                    game_state["victory"] = True
                    game_state["boss_phase"] = "🏆 VITÓRIA! O TIME DE HEROIS VENCEU A VALIDAÇÃO RÍGIDA E DERROTOU O PO VILÃO!"

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(strict_po_lifecycle_game_loop())

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

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
        "kanban": game_state["kanban"],
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
        <title>FLOSE AEOS - Strict PO Validation Kanban Workflow</title>
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
                width: 540px;
                background: #11121d;
                padding: 1.2rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border-left: 4px solid #3b3d54;
                overflow-y: auto;
            }

            .hud-title {
                font-size: 0.7rem;
                color: #55ff55;
                margin-bottom: 0.8rem;
                text-shadow: 2px 2px #00aa00;
            }

            .kanban-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.5rem;
                margin-bottom: 1rem;
            }

            .kanban-col {
                background: rgba(0,0,0,0.5);
                border: 2px solid #30363d;
                border-radius: 6px;
                padding: 0.5rem;
                min-height: 120px;
            }

            .kanban-col-title {
                font-size: 0.45rem;
                font-weight: bold;
                margin-bottom: 0.4rem;
                text-align: center;
            }

            .card-todo { color: #ff5555; }
            .card-validation { color: #ffaa00; }
            .card-done { color: #55ff55; }

            .kanban-card-item {
                background: rgba(255,255,255,0.05);
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 0.4rem;
                margin-bottom: 0.4rem;
                font-size: 0.42rem;
                line-height: 1.3;
            }

            .skill-upgrade-card {
                background: rgba(0,0,0,0.6);
                border: 2px solid #3b3d54;
                border-radius: 6px;
                padding: 0.4rem;
                margin-bottom: 0.3rem;
                font-size: 0.45rem;
            }

            .btn-upgrade {
                font-family: 'Press Start 2P', monospace;
                background: #a855f7;
                color: #fff;
                border: 2px solid #7e22ce;
                padding: 0.3rem 0.5rem;
                font-size: 0.4rem;
                cursor: pointer;
                border-radius: 4px;
                float: right;
            }

            .btn-upgrade:hover { background: #c084fc; }
        </style>
    </head>
    <body>
        <div id="game-container">
            <canvas id="pixel-canvas"></canvas>

            <div class="side-panel">
                <div>
                    <div class="hud-title">📋 KANBAN DO PO CHATO: A FAZER ➔ VALIDAÇÃO ➔ DONE</div>
                    <div style="font-size:0.45rem; color:#9ca3af; margin-bottom:0.8rem;">O PO cria no 'A FAZER', heróis ajustam para 'EM VALIDAÇÃO', PO valida estritamente!</div>

                    <!-- KANBAN BOARD 3 COLUNAS -->
                    <div class="kanban-grid">
                        <div class="kanban-col">
                            <div class="kanban-col-title card-todo">🔴 A FAZER</div>
                            <div id="col-todo"></div>
                        </div>
                        <div class="kanban-col">
                            <div class="kanban-col-title card-validation">🟡 EM VALIDAÇÃO</div>
                            <div id="col-validation"></div>
                        </div>
                        <div class="kanban-col">
                            <div class="kanban-col-title card-done">🟢 CONCLUÍDO</div>
                            <div id="col-done"></div>
                        </div>
                    </div>

                    <div style="font-size:0.5rem; color:#a855f7; margin-bottom:0.4rem;">🛡️ SKILLS DOS HERÓIS:</div>
                    <div id="skills-list">Carregando heróis...</div>
                </div>

                <div>
                    <div style="font-size: 0.45rem; color: #55ff55; margin-bottom: 0.3rem;">📜 AUDIT LOG DE VALIDAÇÕES DO PO</div>
                    <div id="audit-log" style="font-size: 0.4rem; color: #9ca3af; max-height: 80px; overflow-y: auto;"></div>
                </div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pixel-canvas');
            const ctx = canvas.getContext('2d');

            function resizeCanvas() {
                canvas.width = window.innerWidth - 540;
                canvas.height = window.innerHeight;
            }
            resizeCanvas();
            window.addEventListener('resize', resizeCanvas);

            let gameState = {};
            let agentsList = [];

            function drawPixelSprite(x, y, color, name, respMs, healthPct) {
                ctx.fillStyle = color;
                ctx.fillRect(x, y + 10, 24, 20);

                ctx.fillStyle = "#ffcc99";
                ctx.fillRect(x + 4, y, 16, 14);

                ctx.fillStyle = "#000";
                ctx.fillRect(x + 7, y + 4, 3, 3);
                ctx.fillRect(x + 14, y + 4, 3, 3);

                ctx.font = '7px "Press Start 2P"';
                ctx.fillStyle = color;
                ctx.fillText(name, x - 5, y - 10);

                ctx.fillStyle = "#440000";
                ctx.fillRect(x - 6, y - 6, 36, 4);
                ctx.fillStyle = healthPct > 50 ? "#00ff00" : "#ff5555";
                ctx.fillRect(x - 6, y - 6, (36 * healthPct) / 100, 4);

                ctx.font = '5px "Press Start 2P"';
                ctx.fillStyle = "#55ffff";
                ctx.fillText(`${respMs.toFixed(1)}ms`, x - 5, y + 38);
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

                ctx.font = '10px "Press Start 2P"';
                ctx.fillStyle = "#ff5555";
                ctx.fillText("👹 PO CHATO (AUDITOR DE VALIDAÇÃO)", bx - 85, by - 15);

                ctx.fillStyle = "#440000";
                ctx.fillRect(canvas.width / 2 - 150, 15, 300, 16);
                ctx.fillStyle = "#ff3333";
                ctx.fillRect(canvas.width / 2 - 150, 15, (300 * hpPercent) / 100, 16);
                ctx.strokeStyle = "#ffffff";
                ctx.strokeRect(canvas.width / 2 - 150, 15, 300, 16);

                ctx.font = '6px "Press Start 2P"';
                ctx.fillStyle = "#ffaa00";
                ctx.fillText(phaseText.substring(0, 50), canvas.width / 2 - 140, 42);
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
                    drawPOBoss(hpPct, gameState.boss_phase || "Auditando Cards...");

                    agentsList.forEach(a => {
                        drawPixelSprite(a.x, a.y, a.sprite_color, a.name, a.actual_latency_ms, a.health_pct);
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
                const kanban = data.kanban;

                // Render Colunas Kanban
                document.getElementById('col-todo').innerHTML = kanban.to_do.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#ff5555; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 20)}...</div>
                        ${c.rejections > 0 ? `<div style="color:#ff0000; font-size:0.38rem;">⚠️ Barrado ${c.rejections}x!</div>` : ''}
                    </div>
                `).join('');

                document.getElementById('col-validation').innerHTML = kanban.in_validation.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#ffaa00; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 20)}...</div>
                    </div>
                `).join('');

                document.getElementById('col-done').innerHTML = kanban.done.map(c => `
                    <div class="kanban-card-item">
                        <div style="color:#55ff55; font-weight:bold;">${c.id}</div>
                        <div>${c.title.substring(0, 20)}...</div>
                    </div>
                `).join('');

                const keys = ["felipe", "sofia", "lucas", "beatriz"];
                document.getElementById('skills-list').innerHTML = agentsList.map((a, i) => `
                    <div class="skill-upgrade-card">
                        <button class="btn-upgrade" onclick="upgradeSkill('${keys[i]}')">UPGRADE ⬆️</button>
                        <div style="font-weight:bold; color:${a.sprite_color};">${a.name} (Lv.${a.skill_level})</div>
                        <div style="color:#9ca3af; margin-top:0.2rem;">Latência: <span style="color:#55ffff;">${a.actual_latency_ms.toFixed(1)}ms</span></div>
                    </div>
                `).join('');

                document.getElementById('audit-log').innerHTML = data.audit_logs.map(l => `
                    <div style="margin-bottom:0.2rem;">> ${l.action}: ${l.card_id || ''}</div>
                `).join('');
            }

            async function upgradeSkill(key) {
                await fetch(`/api/agents/upgrade_skill?agent_key=${key}`, { method: 'POST' });
                updateState();
            }

            updateState();
            setInterval(updateState, 1200);
        </script>
    </body>
    </html>
    """
