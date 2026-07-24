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

app = FastAPI(title="FLOSE (AEOS) - Web Dashboard & Control Tower")

# Core System Instances
bus = EventBus()
planner = PlanningEngine()
governance = GovernanceEngine()
jira = JiraConnector()

# In-Memory State for Dashboard Demo
agents_db: Dict[str, AgentIdentity] = {
    "agt_ceo": AgentIdentity(agent_id="agt_ceo", role_name="Chief Executive Agent", tier=AgentTier.EXECUTIVE, reputation_score=1.0),
    "agt_arch_01": AgentIdentity(agent_id="agt_arch_01", role_name="Software Architect", tier=AgentTier.ARCHITECTURE, reputation_score=0.98),
    "agt_dev_backend": AgentIdentity(agent_id="agt_dev_backend", role_name="Senior Backend Dev", tier=AgentTier.ENGINEERING, reputation_score=0.94),
    "agt_qa_security": AgentIdentity(agent_id="agt_qa_security", role_name="QA & Security Auditor", tier=AgentTier.QA_SECURITY, reputation_score=0.99),
}

tasks_db: Dict[str, TaskSpecification] = {}
audit_logs: List[Dict[str, Any]] = []

@app.on_event("startup")
async def startup_event():
    await bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()

class GoalCreateRequest(BaseModel):
    goal_id: str
    goal_title: str
    steps: List[str]
    sync_jira: bool = True
    jira_project_key: Optional[str] = "FLO"

class EvidenceAddRequest(BaseModel):
    task_id: str
    evidence_url: str

@app.get("/api/status")
async def get_status():
    return {
        "status": "OPERATIONAL",
        "system": "FLOSE AEOS v0.1.0",
        "active_agents": len(agents_db),
        "total_tasks": len(tasks_db),
        "audit_logs_count": len(audit_logs),
        "jira_status": "CONNECTED" if jira.is_configured else "SIMULATION_MODE"
    }

@app.get("/api/agents")
async def get_agents():
    return list(agents_db.values())

@app.get("/api/tasks")
async def get_tasks():
    return list(tasks_db.values())

@app.get("/api/jira/issues")
async def get_jira_issues():
    return jira.search_issues()

@app.post("/api/goals/decompose")
async def decompose_goal(req: GoalCreateRequest):
    created_tasks = planner.decompose_goal(req.goal_id, req.goal_title, req.steps)
    jira_results = []
    
    for task in created_tasks:
        tasks_db[task.task_id] = task
        
        # Sincronização automática com Jira
        if req.sync_jira:
            j_res = jira.create_issue(
                project_key=req.jira_project_key or "FLO",
                summary=task.title,
                description=task.description
            )
            jira_results.append(j_res)
        
        # Audit Log
        payload_str = task.model_dump_json()
        h = governance.generate_audit_hash("agt_ceo", "TASK_CREATED", payload_str)
        audit_logs.append({
            "event_id": f"evt_{len(audit_logs)+1}",
            "agent_id": "agt_ceo",
            "action": "GOAL_DECOMPOSED",
            "task_id": task.task_id,
            "hash": h,
        })
        
    return {
        "message": f"{len(created_tasks)} tasks criadas com sucesso.",
        "tasks": created_tasks,
        "jira_integration": jira_results
    }

@app.post("/api/tasks/evidence")
async def add_evidence(req: EvidenceAddRequest):
    if req.task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[req.task_id]
    task.evidence_links.append(req.evidence_url)
    valid, msg = governance.validate_evidence(task)
    if valid:
        task.status = TaskStatus.DONE
    return {"valid": valid, "governance_message": msg, "task": task}

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FLOSE (AEOS) - Control Tower & Jira Bridge</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #090d16;
                --card-bg: rgba(18, 26, 43, 0.7);
                --accent: #6366f1;
                --accent-glow: rgba(99, 102, 241, 0.4);
                --success: #10b981;
                --jira-blue: #0052cc;
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
                background: linear-gradient(135deg, #a855f7, #6366f1, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .badges { display: flex; gap: 0.5rem; }

            .badge {
                background: rgba(16, 185, 129, 0.1);
                color: var(--success);
                border: 1px solid rgba(16, 185, 129, 0.3);
                padding: 0.4rem 0.8rem;
                border-radius: 999px;
                font-size: 0.85rem;
                font-weight: 600;
            }

            .badge-jira {
                background: rgba(0, 82, 204, 0.15);
                color: #4c9aff;
                border: 1px solid rgba(0, 82, 204, 0.4);
            }

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
                display: flex;
                align-items: center;
                gap: 0.5rem;
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
                background: linear-gradient(135deg, #6366f1, #4f46e5);
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
                box-shadow: 0 4px 12px var(--accent-glow);
            }

            input, textarea {
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
                <div class="logo">FLOSE AEOS</div>
                <div style="color: var(--text-muted); font-size: 0.9rem;">Agentic Enterprise Operating System - Control Tower & Jira Bridge</div>
            </div>
            <div class="badges">
                <div class="badge">● SYSTEM ONLINE</div>
                <div class="badge badge-jira">🔷 JIRA BRIDGE READY</div>
            </div>
        </header>

        <div class="grid">
            <div class="card">
                <h3>🤖 Organograma de Agentes Ativos</h3>
                <div id="agents-list">Carregando agentes...</div>
            </div>

            <div class="card">
                <h3>🎯 Decompor Objetivo e Sincronizar Jira</h3>
                <input type="text" id="goal-id" placeholder="ID do Objetivo (ex: OBJ-FLO-01)">
                <input type="text" id="goal-title" placeholder="Título (ex: Implementar Auth JWT)">
                <textarea id="goal-steps" rows="2" placeholder="Sub-tasks separadas por vírgula"></textarea>
                <button class="btn" onclick="submitGoal()">Decompor & Gerar Issues Jira</button>
            </div>

            <div class="card">
                <h3>🔷 Jira Board Sync (Issues Remotas)</h3>
                <div id="jira-issues-list">Buscando issues do Jira...</div>
            </div>
        </div>

        <div class="grid">
            <div class="card">
                <h3>📜 Audit Log & Governança (Axioma 1)</h3>
                <pre id="audit-log">Audit log sincronizado.</pre>
            </div>

            <div class="card">
                <h3>📋 Execution Queue (Tasks Internas)</h3>
                <div id="tasks-list">Nenhuma task na fila.</div>
            </div>
        </div>

        <script>
            async function loadData() {
                const agentsRes = await fetch('/api/agents');
                const agents = await agentsRes.json();
                document.getElementById('agents-list').innerHTML = agents.map(a => `
                    <div class="agent-item">
                        <div>
                            <div class="agent-name">${a.agent_id}</div>
                            <div class="agent-role">${a.role_name} (${a.tier})</div>
                        </div>
                        <div style="color: var(--success); font-weight:600;">Score: ${a.reputation_score}</div>
                    </div>
                `).join('');

                const jiraRes = await fetch('/api/jira/issues');
                const jiraIssues = await jiraRes.json();
                document.getElementById('jira-issues-list').innerHTML = jiraIssues.map(i => `
                    <div class="agent-item">
                        <div>
                            <div class="agent-name">${i.key || 'MOCK-1'}: ${i.fields ? i.fields.summary : i.summary}</div>
                            <div class="agent-role">Status: ${i.fields ? i.fields.status.name : 'Simulated'}</div>
                        </div>
                    </div>
                `).join('');

                const tasksRes = await fetch('/api/tasks');
                const tasks = await tasksRes.json();
                document.getElementById('tasks-list').innerHTML = tasks.length ? tasks.map(t => `
                    <div class="agent-item">
                        <div>
                            <div class="agent-name">${t.title}</div>
                            <div class="agent-role">ID: ${t.task_id} | Priority: ${t.priority}</div>
                        </div>
                        <div>
                            <span style="padding: 0.25rem 0.5rem; background: rgba(99,102,241,0.2); border-radius: 4px; font-size:0.8rem;">
                                ${t.status}
                            </span>
                        </div>
                    </div>
                `).join('') : '<div style="color: var(--text-muted); padding: 1rem 0;">Nenhuma task criada.</div>';
            }

            async function submitGoal() {
                const goal_id = document.getElementById('goal-id').value || "OBJ-" + Math.floor(Math.random()*1000);
                const goal_title = document.getElementById('goal-title').value || "Refatoração de Código FLOSE";
                const rawSteps = document.getElementById('goal-steps').value || "Criar Schema, Integrar Jira API, Validar Testes";
                const steps = rawSteps.split(',').map(s => s.trim());

                const res = await fetch('/api/goals/decompose', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ goal_id, goal_title, steps, sync_jira: true, jira_project_key: "FLO" })
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
