import os

with open('src/flose/web_app.py', 'r') as f:
    lines = f.readlines()

def get_line_idx(search_str):
    for i, line in enumerate(lines):
        if search_str in line:
            return i
    return -1

start_idx = get_line_idx('async def dynamic_frenzy_and_training_game_loop():')
end_idx = get_line_idx('async def get_boss_state():')

new_loops = """
async def po_villain_creation_loop():
    \"\"\"
    Escaneia o código-fonte (main branch local) via AST. Se achar smells, cria no Jira na coluna A Fazer.
    \"\"\"
    import asyncio
    await asyncio.sleep(5)
    while True:
        try:
            from flose.agents.po_auditor import scan_host_codebase
            smell = await asyncio.to_thread(scan_host_codebase)
            if smell:
                title, desc = smell
                await async_create_jira_card_background(title, desc)
                game_state["boss_phase"] = f"🔥 PO VILÃO ACHOU DÉBITO E CRIOU CARD: {title[:30]}..."
                audit_logs.append({
                    "event_id": f"evt_{len(audit_logs)+1}",
                    "action": "PO_CREATED_CARD",
                    "title": title
                })
        except Exception as e:
            print(f"[PO Creation Error] {e}")
        await asyncio.sleep(60) # Roda a cada 60 segundos

async def po_villain_validation_loop():
    \"\"\"
    Busca cards em 'Em análise' (Validação) no Jira. Roda pytest local. Aprova ou Rejeita.
    \"\"\"
    import asyncio
    import subprocess
    await asyncio.sleep(10)
    while True:
        try:
            # Puxa issues do Jira que estão em Validação ("Em análise")
            issues = await asyncio.to_thread(jira.fetch_real_jira_issues, "FLOSEUP", 50)
            validation_issues = [i for i in issues if str(i.get("status", "")).upper() in ["EM ANÁLISE", "VALIDATION"]]
            
            for issue in validation_issues:
                card_id = issue.get("id")
                game_state["boss_phase"] = f"⚖️ PO VILÃO ESTÁ VALIDANDO {card_id}..."
                
                # Roda testes localmente
                res = await asyncio.to_thread(subprocess.run, ["pytest", "-v"], cwd=".", capture_output=True, text=True, timeout=60)
                
                if res.returncode == 0:
                    # SUCESSO!
                    safe_jira_comment(card_id, "PO Auditor", f"🚨 [PO Auditor]: ✅ **PO VILÃO APROVOU A SOLUÇÃO!** Testes passaram localmente. Mapeado para Done.\\n\\nLogs:\\n{{quote}}\\n{res.stdout[-500:]}\\n{{quote}}")
                    await asyncio.to_thread(jira.transition_issue, card_id, "Feito")
                    game_state["boss_phase"] = f"✅ PO VILÃO APROVOU {card_id}!"
                    game_state["boss_hp"] -= 150
                else:
                    # FALHA!
                    safe_jira_comment(card_id, "PO Auditor", f"🚨 [PO Auditor]: ❌ **PO VILÃO REJEITOU O CÓDIGO!** Testes falharam. Volte para 'Fazendo' e conserte.\\n\\nLogs de Erro:\\n{{quote}}\\n{res.stdout[-1000:]}\\n{{quote}}")
                    await asyncio.to_thread(jira.transition_issue, card_id, "Fazendo")
                    game_state["boss_phase"] = f"❌ PO VILÃO REJEITOU {card_id}!"
                
                await asyncio.sleep(5)
        except Exception as e:
            print(f"[PO Validation Error] {e}")
        
        await asyncio.sleep(30) # Roda a cada 30 segundos

@app.on_event("startup")
async def start_autonomous_loop():
    await bus.start()
    asyncio.create_task(auto_save_persistence_loop())
    asyncio.create_task(po_villain_creation_loop())
    asyncio.create_task(po_villain_validation_loop())

@app.on_event("shutdown")
async def shutdown_event():
    await bus.stop()
    save_game_state()
    print("[FloseUP Boss Server] Desligado com segurança e estado salvo!")

"""

if start_idx != -1 and end_idx != -1:
    new_content = "".join(lines[:start_idx]) + new_loops + "".join(lines[end_idx:])
    with open('src/flose/web_app.py', 'w') as f:
        f.write(new_content)
    print("Injected safely!")
else:
    print("Could not find indices!")
