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

app = FastAPI(title="FLOSE (AEOS) - Web Dashboard & Control Tower")

# Core System & Connectors Instances
bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()
gemma = GemmaLocalConnector()

agents_db: Dict[str, AgentIdentity] = {
    "agt_ceo": AgentIdentity(agent_id="agt_ceo", role_name="Chief Executive Agent", tier=AgentTier.EXECUTIVE, reputation_score=1.0),
    "agt_gemma_idea": AgentIdentity(agent_id="agt_gemma_idea", role_name="Gemma 4 Local Idea Generator", tier=AgentTier.EXECUTIVE, reputation_score=0.97),
    "agt_claude_coder": AgentIdentity(agent_id="agt_claude_coder", role_name="Claude Code & AGY Coder Agent", tier=AgentTier.ENGINEERING, reputation_score=0.99),
    "agt_qa_security": AgentIdentity(agent_id="agt_qa_security", role_name="QA & Security Auditor", tier=AgentTier.QA_SECURITY, reputation_score=0.99),
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
    domain_prompt: str = "Arquitetura Multiagente e Governança Corporativa"
    sync_jira: bool = True

@app.get("/api/status")
async def get_status():
    return {
        "status": "OPERATIONAL",
        "system": "FLOSE AEOS v0.1.0",
        "gemma_local_engine": "ACTIVE",
        "claude_agy_coder": "READY",
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
    # 1. Gerar Ideias via Gemma 4 Local
    generated = gemma.generate_ideas(req.domain_prompt)
    jira_created = []
    
    for idx, idea in enumerate(generated, start=1):
        ideas_db.append(idea)
        
        # 2. Decompor Ideia em Tasks de Código via Planning Engine
        steps = [
            f"Conceituar {idea['title']} no modelo Pydantic",
            f"Claude Code & AGY: Codificar {idea['title']} em Python",
            f"Governance Engine: Validar evidência de execução e suíte de testes"
        ]
        created_tasks = planner.decompose_goal(f"IDEA_{idx}", idea["title"], steps)
        
        for task in created_tasks:
            tasks_db[task.task_id] = task
            
            # 3. Registrar tudo no Jira
            if req.sync_jira:
                j_res = jira.create_issue(
                    project_key="FLO",
                    summary=f"[FLOSE-Gemma4] {task.title}",
                    description=f"Ideia gerada pelo Gemma 4 Local.\n\nDetalhes: {idea['summary']}\nStack: {idea.get('technical_stack')}\n\nTask de Código atribuída ao Claude Code & AGY Coder Agent."
                )
                jira_created.append(j_res)
            
            # 4. Registrar em Audit Log imutável
            payload_str = task.model_dump_json()
            h = governance.generate_audit_hash("agt_gemma_idea", "IDEA_GENERATED_AND_CODED", payload_str)
            audit_logs.append({
                "event_id": f"evt_{len(audit_logs)+1}",
                "agent_id": "agt_gemma_idea",
                "coder_agent": "agt_claude_coder",
                "action": "IDEA_CREATED_AND_REGISTERED_IN_JIRA",
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
        <title>FLOSE (AEOS) - Gemma 4 + Claude Code + AGY + Jira Pipeline</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #090d16;
                --card-bg: rgba(18, 26, 43, 0.7);
                --accent: #6366f1;
                --accent-glow: rgba(99, 102, 241, 0.4);
                --success: #10b981;
                --gemma: #ec4899;
                --claude: #f97316;
                --jira: #3b82f6;
                --text: #f3f4f6;
                --text-muted: #9ca3af;
                --border: rgba(255, 255, 255, 0.1);
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg);
                color: var(--text);
                padding: 2rem;
                min-height: 100vh;
            }

            header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
                padding-bottom: 1rem;
                border-bottom: 1px solid var(--border);
            }

            .logo {
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #ec4899, #f97316, #6366f1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .badges { display: flex; gap: 0.5rem; }

            .badge {
                padding: 0.4rem 0.8rem;
                border-radius: 999px;
                font-size: 0.85rem;
                font-weight: 600;
            }

            .badge-gemma { background: rgba(236, 72, 153, 0.15); color: var(--gemma); border: 1px solid rgba(236, 72, 153, 0.4); }
            .badge-claude { background: rgba(249, 115, 22, 0.15); color: var(--claude); border: 1px solid rgba(249, 115, 22, 0.4); }
            .badge-jira { background: rgba(59, 130, 246, 0.15); color: var(--jira); border: 1px solid rgba(59, 130, 246, 0.4); }

            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .card {
                background: var(--card-bg);
                backdrop-filter: blur(12px);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }

            .card h3 {
                font-size: 1.2rem;
                margin-bottom: 1rem;
                color: var(--text);
            }

            .agent-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.75rem 0;
                border-bottom: 1px solid var(--border);
            }

            .agent-item:last-child { border-bottom: none; }

            .agent-name { font-weight: 600; }
            .agent-role { font-size: 0.85rem; color: var(--text-muted); }

            .btn {
                background: linear-gradient(135deg, #ec4899, #f97316);
                color: white;
                border: none;
                padding: 0.75rem 1.25rem;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                width: 100%;
                margin-top: 1rem;
            }

            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
            }

            input {
                width: 100%;
                padding: 0.75rem;
                background: rgba(0,0,0,0.3);
                border: 1px solid var(--border);
                border-radius: 8px;
                color: white;
                margin-bottom: 0.75rem;
                font-family: inherit;
            }

            pre {
                font-family: 'JetBrains Mono', monospace;
                background: rgba(0,0,0,0.4);
                padding: 1rem;
                border-radius: 8px;
                overflow-x: auto;
                font-size: 0.85rem;
                color: #e5e7eb;
                max-height: 250px;
            }
        </style>
    </head>
    <body>
        <header>
            <div>
                <div class="logo">FLOSE AEOS PIPELINE</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">Gemma 4 Local Ideas ➔ Claude Code & AGY Coder ➔ Jira Sync</div>
            </div>
            <div class="badges">
                <div class="badge badge-gemma">🤖 GEMMA 4 LOCAL</div>
                <div class="badge badge-claude">⚡ CLAUDE CODE & AGY</div>
                <div class="badge badge-jira">🔷 JIRA SYNC</div>
            </div>
        </header>

        <div class="grid">
            <div class="card">
                <h3>💡 1. Gerar Ideias com Gemma 4 Local</h3>
                <input type="text" id="domain-prompt" value="Inovação Multiagente e Governança de Tokens">
                <button class="btn" onclick="triggerPipeline()">Disparar Pipeline (Ideia ➔ Código ➔ Jira)</button>
            </div>

            <div class="card">
                <h3>🧠 2. Ideias Produzidas (Gemma 4 Engine)</h3>
                <div id="ideas-list">Nenhuma ideia gerada ainda.</div>
            </div>

            <div class="card">
                <h3>📜 3. Audit Log & Registros no Jira</h3>
                <pre id="audit-log">Aguardando disparo do pipeline...</pre>
            </div>
        </div>

        <script>
            async function loadData() {
                const ideasRes = await fetch('/api/ideas');
                const ideas = await ideasRes.json();
                document.getElementById('ideas-list').innerHTML = ideas.length ? ideas.map(i => `
                    <div class="agent-item">
                        <div>
                            <div class="agent-name" style="color:var(--gemma);">${i.title}</div>
                            <div class="agent-role">${i.summary}</div>
                        </div>
                        <div style="color: var(--claude); font-weight:600; font-size:0.8rem;">${i.jira_priority || 'High'}</div>
                    </div>
                `).join('') : '<div style="color: var(--text-muted); padding: 1rem 0;">Nenhuma ideia gerada.</div>';
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
