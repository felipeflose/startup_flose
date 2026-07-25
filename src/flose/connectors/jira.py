import os
import ssl
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.parse
import json
import base64

def load_env_file():
    """Loads variables from .env file into os.environ."""
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()

load_env_file()

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

class JiraConnector:
    """Connector for REAL Jira Cloud API with Detailed Epic/Task Creation."""

    def __init__(self):
        load_env_file()
        host = os.environ.get("JIRA_HOST", "")
        if "atlassian.net" in host:
            self.domain = host.replace("https://", "").replace("http://", "").replace(".atlassian.net", "").strip("/")
        else:
            self.domain = os.environ.get("JIRA_DOMAIN", "felipeflose")
            
        self.email = os.environ.get("JIRA_USER") or os.environ.get("JIRA_EMAIL", "")
        self.api_token = os.environ.get("JIRA_TOKEN") or os.environ.get("JIRA_API_TOKEN", "")

    @property
    def is_configured(self) -> bool:
        return bool(self.domain and self.email and self.api_token)

    def _get_headers(self) -> Dict[str, str]:
        auth_str = f"{self.email}:{self.api_token}"
        b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        return {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def delete_issue(self, issue_key: str) -> bool:
        if not self.is_configured: return True
        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}"
        req = urllib.request.Request(url, headers=self._get_headers(), method="DELETE")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                return resp.status in (200, 204)
        except Exception:
            return False

    def transition_issue(self, issue_key: str, target_status_name: str) -> bool:
        """Busca as transições válidas e move o card para o status desejado (ex: 'Done' ou 'Concluído')."""
        if not self.is_configured: return True
        
        # 1. Obter transições disponíveis para esse card
        url_get = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/transitions"
        req_get = urllib.request.Request(url_get, headers=self._get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req_get, context=ssl_context, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                transitions = data.get("transitions", [])
                
                target_id = None
                # Procura transição que contenha o termo (case insensitive)
                for t in transitions:
                    t_name = t.get("name", "").lower()
                    if target_status_name.lower() in t_name or "conclu" in t_name or "done" in t_name:
                        target_id = t.get("id")
                        break
                
                if not target_id:
                    print(f"[Jira Transition] Status alvo '{target_status_name}' não encontrado para {issue_key}.")
                    return False
                
                # 2. Faz o POST para transacionar
                payload = {"transition": {"id": target_id}}
                req_post = urllib.request.Request(url_get, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
                with urllib.request.urlopen(req_post, context=ssl_context, timeout=10) as resp_post:
                    print(f"[Jira Transition] Card {issue_key} movido para {target_status_name} com sucesso!")
                    return resp_post.status in (200, 204)
        except Exception as e:
            print(f"[Jira Transition Error] {e}")
            return False

    def fetch_real_jira_issues(self, project_key: str = "KAN", limit: int = 10) -> List[Dict[str, Any]]:
        """Busca as issues REAIS e seus detalhes na conta felipeflose.atlassian.net do Jira."""
        if not self.is_configured:
            return []

        url = f"https://{self.domain}.atlassian.net/rest/api/3/search/jql?jql=project={project_key}"
        req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
        issues_result = []
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_issues = data.get("issues", [])[:limit]
                
                for item in raw_issues:
                    issue_id = item.get("id")
                    detail_url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_id}?expand=renderedFields,comments"
                    d_req = urllib.request.Request(detail_url, headers=self._get_headers(), method="GET")
                    try:
                        with urllib.request.urlopen(d_req, context=ssl_context, timeout=5) as d_resp:
                            d_data = json.loads(d_resp.read().decode("utf-8"))
                            comments = []
                            c_data = d_data.get("fields", {}).get("comment", {}).get("comments", [])
                            for c in c_data:
                                author = c.get("author", {}).get("displayName", "Agente")
                                body = c.get("body", {}).get("content", [{}])[0].get("content", [{}])[0].get("text", "Comentário") if isinstance(c.get("body"), dict) else str(c.get("body"))
                                comments.append({"author": author, "text": body})

                            issues_result.append({
                                "id": d_data.get("key"),
                                "title": d_data.get("fields", {}).get("summary", "Card sem título"),
                                "status": "A FAZER",
                                "type": "Card Real Jira Cloud",
                                "comments": comments,
                                "rejections": 0
                            })
                    except Exception:
                        continue
        except Exception as e:
            print(f"[Jira Fetch Error] {e}")
            
        return issues_result

    def create_detailed_epic_or_task(self, project_key: str, summary: str, detailed_description: str, epic_name: str = "ÉPICO PO VILÃO") -> Dict[str, Any]:
        """Cria um Card REAL e EXTREMAMENTE DETALHADO no Jira Cloud da sua conta!"""
        if not self.is_configured:
            return {"mock": True, "summary": summary}

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue"
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": f"[PO-EVIL-BOSS] {summary}",
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "heading",
                            "attrs": {"level": 2},
                            "content": [{"type": "text", "text": f"🎯 Épico do PO Vilão: {epic_name}"}]
                        },
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": detailed_description}]
                        },
                        {
                            "type": "heading",
                            "attrs": {"level": 3},
                            "content": [{"type": "text", "text": "📋 Critérios de Aceite & DoD (Definition of Done):"}]
                        },
                        {
                            "type": "bulletList",
                            "content": [
                                {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Alinhamento Pixel Perfect 100% verificado em 2D/3D Canvas."}]}]},
                                {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Refatoração Backend Async sem estouro de janela de contexto."}]}]},
                                {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Resposta do time antes do limite de Timeout do PO."}]}]}
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Task"}
            }
        }
        
        # Se for passado um ID de épico KAN-XXX, cria o vínculo de sub-tarefa / parent.
        if epic_name.startswith("KAN-"):
            payload["fields"]["parent"] = {"key": epic_name.strip()}

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"[Jira Success] Issue Criada no Jira Real com Sucesso! Key: {data.get('key')}")
                return data
        except Exception as e:
            print(f"[Jira Create Error] {e}")
            return {"error": str(e)}

    def add_comment(self, issue_key: str, author_name: str, comment_text: str) -> Dict[str, Any]:
        if not self.is_configured:
            return {"mock": True, "comment": comment_text}

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/comment"
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": f"[{author_name}]: {comment_text}"}]
                }]
            }
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def transition_issue(self, issue_key: str, transition_name: str) -> bool:
        """Transiciona um card no Jira (Ex: To Do -> In Progress -> Done)"""
        if not self.is_configured:
            return True
            
        # 1. Pega os IDs de transição possíveis para este card
        url_transitions = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/transitions"
        req_trans = urllib.request.Request(url_transitions, headers=self._get_headers(), method="GET")
        
        transition_id = None
        try:
            with urllib.request.urlopen(req_trans, context=ssl_context, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                # Mapeamentos amigáveis
                target_names = [transition_name.lower()]
                if transition_name.lower() == "done":
                    target_names.append("concluído")
                
                for t in data.get("transitions", []):
                    t_name = t.get("name", "").lower()
                    if any(tn in t_name for tn in target_names):
                        transition_id = t.get("id")
                        break
        except Exception as e:
            print(f"[Jira Transition Error] Falha ao buscar transições: {e}")
            return False
            
        if not transition_id:
            print(f"[Jira Transition Error] Transição '{transition_name}' não encontrada para o card {issue_key}")
            return False
            
        # 2. Executa a transição
        payload = {"transition": {"id": transition_id}}
        req = urllib.request.Request(url_transitions, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                return resp.status in (200, 204)
        except Exception as e:
            print(f"[Jira Transition Error] Falha ao transicionar: {e}")
            return False
