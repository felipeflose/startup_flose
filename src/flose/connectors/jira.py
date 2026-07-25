import os
import ssl
import json
import base64
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

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
    """Connector for REAL Jira Cloud API with Detailed Epic/Task Creation and Comments."""

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
        if not self.is_configured: 
            return True
        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}"
        req = urllib.request.Request(url, headers=self._get_headers(), method="DELETE")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                return resp.status in (200, 204)
        except Exception:
            return False

    def fetch_real_jira_issues(self, project_key: str = "KAN", limit: int = 1000) -> List[Dict[str, Any]]:
        """Busca os cards REAIS no Jira Cloud utilizando paginação automática (startAt)."""
        if not self.is_configured:
            return []

        issues_result = []
        start_at = 0
        max_per_page = 100

        while len(issues_result) < limit:
            url = f"https://{self.domain}.atlassian.net/rest/api/3/search/jql?jql=project={project_key}%20AND%20status%20!=%20Conclu%C3%ADdo&startAt={start_at}&maxResults={max_per_page}&fields=summary,status,comment"
            req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
            try:
                with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    raw_issues = data.get("issues", [])
                    if not raw_issues:
                        break
                    
                    for item in raw_issues:
                        issue_key = item.get("key")
                        fields = item.get("fields", {})
                        summary = fields.get("summary", "Card sem título")
                        
                        comments = []
                        c_data = fields.get("comment", {}).get("comments", [])
                        for c in c_data:
                            author = c.get("author", {}).get("displayName", "Agente")
                            body = c.get("body", {}).get("content", [{}])[0].get("content", [{}])[0].get("text", "Comentário") if isinstance(c.get("body"), dict) else str(c.get("body"))
                            comments.append({"author": author, "text": body})

                        issues_result.append({
                            "id": issue_key,
                            "title": summary,
                            "status": "A FAZER",
                            "type": "Card Real Jira Cloud",
                            "comments": comments,
                            "rejections": 0
                        })

                    start_at += len(raw_issues)
                    if len(raw_issues) < max_per_page:
                        break
            except Exception as e:
                print(f"[Jira Fetch Error] {e}")
                break
            
        return issues_result

    def create_detailed_epic_or_task(self, project_key: str, summary: str, detailed_description: str, epic_name: str = "ÉPICO PO VILÃO") -> Dict[str, Any]:
        """Cria um Card detalhado no Jira Cloud."""
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
        
        if epic_name.startswith("KAN-"):
            payload["fields"]["parent"] = {"key": epic_name.strip()}

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                print(f"[Jira Success] Issue Criada com Sucesso! Key: {data.get('key')}")
                return data
        except Exception as e:
            print(f"[Jira Create Error] {e}")
            return {"error": str(e)}

    def add_comment(self, issue_key: str, comment_text: str, author_name: str = "FLOSE Agent") -> Dict[str, Any]:
        """
        Adiciona um comentário no Jira Cloud. 
        Suporta chamadas flexíveis: add_comment(issue_key, comment_text) ou add_comment(issue_key, author_name, comment_text).
        """
        if not self.is_configured:
            return {"mock": True, "comment": comment_text}

        # Se for chamado na ordem legada (issue_key, author_name, comment_text), ajusta dinamicamente
        display_text = f"[{author_name}]: {comment_text}" if author_name != "FLOSE Agent" else comment_text

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/comment"
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": display_text}]
                }]
            }
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                print(f"[Jira Comment Success] Comentário publicado em {issue_key}!")
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[Jira Comment Error] {e}")
            return {"error": str(e)}

    def transition_issue(self, issue_key: str, transition_name: str) -> bool:
        """Transiciona um card no Jira (Ex: To Do -> In Progress -> In Validation -> Done)."""
        if not self.is_configured:
            return True
            
        url_transitions = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/transitions"
        req_trans = urllib.request.Request(url_transitions, headers=self._get_headers(), method="GET")
        
        transition_id = None
        try:
            with urllib.request.urlopen(req_trans, context=ssl_context, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                target_names = [transition_name.lower()]
                if transition_name.lower() == "done":
                    target_names.extend(["concluído", "concluido", "done"])
                elif transition_name.lower() == "in progress":
                    target_names.extend(["em andamento", "em progresso", "in progress"])
                elif transition_name.lower() == "in validation":
                    target_names.extend(["em análise", "em analise", "validação", "validacao", "review", "in validation"])
                elif transition_name.lower() == "to do":
                    target_names.extend(["a fazer", "to-do", "to do"])
                
                for t in data.get("transitions", []):
                    t_name = t.get("name", "").lower()
                    if any(tn in t_name for tn in target_names):
                        transition_id = t.get("id")
                        break
        except Exception as e:
            print(f"[Jira Transition Error] Falha ao buscar transições para {issue_key}: {e}")
            return False
            
        if not transition_id:
            print(f"[Jira Transition Error] Transição '{transition_name}' não encontrada para o card {issue_key}")
            return False
            
        payload = {"transition": {"id": transition_id}}
        req = urllib.request.Request(url_transitions, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                print(f"[Jira Transition Success] {issue_key} -> {transition_name}")
                return resp.status in (200, 204)
        except Exception as e:
            print(f"[Jira Transition Error] Falha ao transicionar {issue_key}: {e}")
            return False