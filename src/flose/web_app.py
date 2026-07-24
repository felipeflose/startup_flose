import asyncio
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

app = FastAPI(title="FLOSE (AEOS) - Minecraft 3D Control Tower")

# Core System Instances
bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

# Organograma com Nomes de Pessoas Reais (Estilo Minecraft Voxel)
agents_db: Dict[str, AgentIdentity] = {
    "agt_felipe": AgentIdentity(agent_id="agt_felipe", role_name="Felipe (CEO & Architect Leader)", tier=AgentTier.EXECUTIVE, reputation_score=1.0),
    "agt_gemma_sofia": AgentIdentity(agent_id="agt_gemma_sofia", role_name="Sofia (Gemma 4 Local Idea Engine)", tier=AgentTier.EXECUTIVE, reputation_score=0.98),
    "agt_claude_lucas": AgentIdentity(agent_id="agt_claude_lucas", role_name="Lucas (Claude Code & AGY Master Coder)", tier=AgentTier.ENGINEERING, reputation_score=0.99),
    "agt_beatriz_qa": AgentIdentity(agent_id="agt_beatriz_qa", role_name="Beatriz (QA & Security Guardian)", tier=AgentTier.QA_SECURITY, reputation_score=0.97),
}

tasks_db: Dict[str, TaskSpecification] = {}
audit_logs: List[Dict[str, Any]] = []
ideas_db: List[Dict[str, Any]] = []

@app.on_event("startup")
async def startup_event():
    await bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

class IdeaGenerateRequest(BaseModel):
    domain_prompt: str = "Inovação Multiagente e Governança de Tokens"
    sync_jira: bool = True

@app.get("/api/status")
async def get_status():
    return {
        "status": "OPERATIONAL",
        "system": "FLOSE AEOS v0.1.0 (Minecraft 3D Edition)",
        "gemma_local_engine": "ACTIVE (Sofia)",
        "claude_coder": "ACTIVE (Lucas)",
        "qa_security": "ACTIVE (Beatriz)",
        "ceo_architect": "ACTIVE (Felipe)",
        "jira_status": "CONNECTED" if jira.is_configured else "SIMULATION_MODE",
        "active_agents": len(agents_db),
        "total_ideas": len(ideas_db),
        "total_tasks": len(tasks_db),
    }

@app.get("/api/agents")
async def get_agents():
    return list(agents_db.values())

@app.get("/api/ideas")
async def get_ideas():
    return ideas_db

@app.post("/api/ideas/generate")
async def generate_ideas_and_code(req: IdeaGenerateRequest):
    generated = gemma.generate_ideas(req.domain_prompt)
    jira_created = []
    
    for idx, idea in enumerate(generated, start=1):
        ideas_db.append(idea)
        
        steps = [
            f"Conceituar {idea['title']} no modelo Pydantic (por Sofia & Felipe)",
            f"Codificar {idea['title']} em Python (por Lucas via Claude Code & AGY)",
            f"Validar testes e evidências (por Beatriz QA)"
        ]
        created_tasks = planner.decompose_goal(f"IDEA_{idx}", idea["title"], steps)
        
        for task in created_tasks:
            tasks_db[task.task_id] = task
            
            if req.sync_jira:
                j_res = jira.create_issue(
                    project_key="FLO",
                    summary=f"[FLOSE-Gemma4] {task.title}",
                    description=f"Ideia gerada pela agente Sofia (Gemma 4 Local).\n\nResumo: {idea['summary']}\nResponsável por codificar: Lucas (Claude Code & AGY).\nAuditora: Beatriz (QA)."
                )
                jira_created.append(j_res)
            
            payload_str = task.model_dump_json()
            h = governance.generate_audit_hash("agt_gemma_sofia", "IDEA_GENERATED_AND_CODED", payload_str)
            audit_logs.append({
                "event_id": f"evt_{len(audit_logs)+1}",
                "agent_id": "agt_gemma_sofia (Sofia)",
                "coder_agent": "agt_claude_lucas (Lucas)",
                "action": "MINECRAFT_VOXEL_IDEA_REGISTERED_IN_JIRA",
                "idea_title": idea["title"],
                "hash": h,
            })
            
    return {
        "status": "SUCCESS",
        "ideas_generated": generated,
        "jira_issues_created": jira_created,
        "tasks_in_queue": len(created_tasks)
    }

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE (AEOS) - Minecraft 3D Voxel World</title>
        <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #0d1117;
                --card-bg: rgba(22, 27, 34, 0.85);
                --mc-green: #55ff55;
                --mc-aqua: #55ffff;
                --mc-gold: #ffaa00;
                --mc-red: #ff5555;
                --mc-purple: #aa00aa;
                --border: #30363d;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg);
                color: #c9d1d9;
                padding: 2rem;
                min-height: 100vh;
                background-image: radial-gradient(#21262d 1px, transparent 1px);
                background-size: 16px 16px;
            }

            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
                padding-bottom: 1rem;
                border-bottom: 2px dashed var(--border);
            }

            .logo {
                font-family: 'Press Start 2P', monospace;
                font-size: 1.4rem;
                color: var(--mc-green);
                text-shadow: 3px 3px #00aa00;
            }

            .badges { display: flex; gap: 0.5rem; }

            .badge {
                font-family: 'Press Start 2P', monospace;
                padding: 0.5rem 0.8rem;
                border-radius: 4px;
                font-size: 0.65rem;
                box-shadow: 3px 3px 0px #000;
            }

            .badge-felipe { background: #00a; color: #fff; }
            .badge-sofia { background: #a0a; color: #fff; }
            .badge-lucas { background: #f50; color: #fff; }
            .badge-beatriz { background: #0a0; color: #fff; }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .card {
                background: var(--card-bg);
                border: 3px solid var(--border);
                border-radius: 8px;
                padding: 1.5rem;
                box-shadow: 6px 6px 0px #000;
            }

            .card h3 {
                font-family: 'Press Start 2P', monospace;
                font-size: 0.85rem;
                margin-bottom: 1rem;
                color: var(--mc-gold);
                text-shadow: 2px 2px #553300;
            }

            .agent-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.75rem;
                background: rgba(0,0,0,0.4);
                border: 2px solid #21262d;
                border-radius: 4px;
                margin-bottom: 0.5rem;
            }

            .agent-name { font-weight: 700; color: var(--mc-aqua); }
            .agent-role { font-size: 0.85rem; color: #8b949e; }

            .btn {
                font-family: 'Press Start 2P', monospace;
                background: #55ff55;
                color: #000;
                border: 3px solid #00aa00;
                padding: 0.85rem;
                font-size: 0.7rem;
                cursor: pointer;
                box-shadow: 4px 4px 0px #000;
                width: 100%;
                margin-top: 1rem;
                transition: transform 0.1s;
            }

            .btn:active {
                transform: translate(2px, 2px);
                box-shadow: 2px 2px 0px #000;
            }

            input {
                width: 100%;
                padding: 0.75rem;
                background: #000;
                border: 2px solid var(--border);
                color: var(--mc-green);
                font-family: 'Press Start 2P', monospace;
                font-size: 0.7rem;
                margin-bottom: 0.75rem;
                border-radius: 4px;
            }

            pre {
                font-family: 'Courier New', monospace;
                background: #000;
                padding: 1rem;
                border: 2px solid var(--border);
                color: var(--mc-green);
                max-height: 250px;
                overflow-x: auto;
                font-size: 0.8rem;
            }
        </style>
    </head>
    <body>
        <header>
            <div>
                <div class="logo">⛏️ FLOSE MINECRAFT 3D</div>
                <div style="color: #8b949e; font-size: 0.9rem; margin-top:0.4rem;">Voxel Agents: Felipe | Sofia | Lucas | Beatriz</div>
            </div>
            <div class="badges">
                <div class="badge badge-felipe">FELIPE (CEO)</div>
                <div class="badge badge-sofia">SOFIA (GEMMA4)</div>
                <div class="badge badge-lucas">LUCAS (CLAUDE/AGY)</div>
                <div class="badge badge-beatriz">BEATRIZ (QA)</div>
            </div>
        </header>

        <div class="grid">
            <div class="card">
                <h3>👥 1. Time de Agentes Voxel</h3>
                <div id="agents-list">Carregando pessoas...</div>
            </div>

            <div class="card">
                <h3>⚡ 2. Criar Ideias (Gemma 4 Local)</h3>
                <input type="text" id="domain-prompt" value="Inovacao Multiagente 3D">
                <button class="btn" onclick="triggerPipeline()">⛏️ MINAR IDEIAS & GERAR CODIGO</button>
            </div>

            <div class="card">
                <h3>📜 3. Audit Log (Redstone Hashes)</h3>
                <pre id="audit-log">Aguardando mineração...</pre>
            </div>
        </div>

        <div class="card">
            <h3>💡 4. Ideias Produzidas & Registradas no Jira</h3>
            <div id="ideas-list">Nenhuma ideia minerada ainda.</div>
        </div>

        <script>
            async function loadData() {
                const agentsRes = await fetch('/api/agents');
                const agents = await agentsRes.json();
                document.getElementById('agents-list').innerHTML = agents.map(a => `
                    <div class="agent-item">
                        <div>
                            <div class="agent-name">⛏️ ${a.role_name}</div>
                            <div class="agent-role">Tier: ${a.tier}</div>
                        </div>
                        <div style="color: var(--mc-gold); font-weight:700;">${a.reputation_score * 100}% HP</div>
                    </div>
                `).join('');

                const ideasRes = await fetch('/api/ideas');
                const ideas = await ideasRes.json();
                document.getElementById('ideas-list').innerHTML = ideas.length ? ideas.map(i => `
                    <div class="agent-item">
                        <div>
                            <div class="agent-name" style="color:var(--mc-gold);">${i.title}</div>
                            <div class="agent-role">${i.summary}</div>
                        </div>
                        <div style="color: var(--mc-aqua); font-weight:bold;">[Jira: ${i.jira_priority || 'High'}]</div>
                    </div>
                `).join('') : '<div style="color: #8b949e; padding: 1rem 0;">Nenhuma ideia minerada.</div>';
            }

            async function triggerPipeline() {
                const domain_prompt = document.getElementById('domain-prompt').value;
                const res = await fetch('/api/ideas/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ domain_prompt, sync_jira: true })
                });
                const data = await res.json();
                document.getElementById('audit-log').innerText = JSON.stringify(data, null, 2);
                loadData();
            }

            loadData();
            setInterval(loadData, 4000);
        </script>
    </body>
    </html>
    """
