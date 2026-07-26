import os
import ssl
from datetime import datetime
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
        # Mapping de termos de transição para cobrir Boards em PT e EN (Fazendo, Em análise, Feito, A fazer)
        target_lower = target_status_name.lower()
        if any(k in target_lower for k in ["progress", "fazendo", "andamento", "dev"]):
            keywords = ["fazendo", "progress", "andamento", "dev"]
        elif any(k in target_lower for k in ["validat", "análise", "analise", "review"]):
            keywords = ["análise", "analise", "validation", "review"]
        elif any(k in target_lower for k in ["done", "conclu", "feito"]):
            keywords = ["feito", "done", "concluí", "conclui"]
        else:
            keywords = ["a fazer", "to do", "todo"]

        try:
            with urllib.request.urlopen(req_get, context=ssl_context, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                transitions = data.get("transitions", [])
                
                target_id = None
                for t in transitions:
                    t_name = (t.get("name") or "").lower()
                    to_status = ((t.get("to") or {}).get("name") or "").lower()
                    if any(kw in t_name or kw in to_status for kw in keywords):
                        target_id = t.get("id")
                        break
                
                if not target_id:
                    print(f"[Jira Transition] Status alvo '{target_status_name}' não encontrado. Transições disponíveis: {transitions} para {issue_key}.")
                    return False
                
                # 2. Faz o POST para transacionar
                payload = {"transition": {"id": target_id}}
                req_post = urllib.request.Request(url_get, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
                with urllib.request.urlopen(req_post, context=ssl_context, timeout=10) as resp_post:
                    print(f"[Jira Transition] Card {issue_key} movido para {target_status_name} com sucesso!")
                    return resp_post.status in (200, 204)
        except Exception as e:
            import traceback
            print(f"[Jira Transition Exception] {e}")
            traceback.print_exc()
            return False

    def fetch_real_jira_issues(self, project_key: str = "FLOSEUP", limit: int = 1000) -> List[Dict[str, Any]]:
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
                            "rejections": 0,
                            "is_new_ast_card": True,
                            "created_at": datetime.now().isoformat()
                        })

                    start_at += len(raw_issues)
                    if len(raw_issues) < max_per_page:
                        break
            except Exception as e:
                print(f"[Jira Fetch Error] {e}")
                break
            
        return issues_result

    def get_or_create_epic(self, project_key: str = "FLOSEUP", epic_name: str = "ÉPICO MESTRE AST STAGE 1") -> Optional[str]:
        """Busca ou cria um Épico PAI no Jira Cloud para vincular todos os cards como filhos."""
        if not self.is_configured:
            return None

        if epic_name.startswith("FLOSEUP-") or epic_name.startswith("KAN-"):
            return epic_name.strip()

        # 1. Tenta buscar um Épico com o nome especificado
        jql = f'project={project_key} AND issuetype=Epic AND summary ~ "{epic_name}"'
        url_search = f"https://{self.domain}.atlassian.net/rest/api/3/search/jql?jql={urllib.parse.quote(jql)}"
        req_search = urllib.request.Request(url_search, headers=self._get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req_search, context=ssl_context, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                issues = data.get("issues", [])
                if issues:
                    epic_key = issues[0].get("key")
                    if epic_key:
                        return epic_key
        except Exception as e:
            print(f"[Jira Epic Search Error] {e}")

        # 2. Se não existir, cria o Épico PAI
        url_create = f"https://{self.domain}.atlassian.net/rest/api/3/issue"
        payload_epic = {
            "fields": {
                "project": {"key": project_key},
                "summary": epic_name,
                "issuetype": {"name": "Epic"},
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text", "text": f"🏆 Épico Pai Mestre do Projeto FLOSEUP: {epic_name}"}]
                    }]
                }
            }
        }
        req_create = urllib.request.Request(url_create, data=json.dumps(payload_epic).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req_create, context=ssl_context, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                epic_key = data.get("key")
                print(f"[Jira Parent Epic Created] Épico PAI Real Criado no Jira: {epic_key} ({epic_name})")
                return epic_key
        except Exception as e:
            print(f"[Jira Parent Epic Create Error] {e}")

        return None

    def create_detailed_epic_or_task(self, project_key: str = "FLOSEUP", summary: str = "", detailed_description: str = "", epic_name: str = "ÉPICO PO VILÃO STAGE 1") -> Dict[str, Any]:
        """Cria um Card REAL e EXTREMAMENTE DETALHADO no Jira Cloud vinculado ao Épico PAI!"""
        if not self.is_configured:
            return {"mock": True, "summary": summary}

        # Garante a existência do Épico PAI no Jira
        parent_epic_key = self.get_or_create_epic(project_key, epic_name)

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue"
        for itype in ["Tarefa", "Task", "História"]:
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
                    "issuetype": {"name": itype}
                }
            }
            
            if parent_epic_key:
                payload["fields"]["parent"] = {"key": parent_epic_key}

            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
            try:
                with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    print(f"[Jira Success] Issue Criada no Jira Real ({project_key}) vinculada ao Épico PAI {parent_epic_key}! Key: {data.get('key')}")
                    return data
            except Exception as e:
                continue

        return {"error": "Não foi possível criar issue no Jira"}

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
                elif transition_name.lower() == "in progress":
                    target_names.extend(["em andamento", "em progresso"])
                elif transition_name.lower() == "in validation":
                    target_names.extend(["em análise", "validação", "review"])
                elif transition_name.lower() == "to do":
                    target_names.extend(["a fazer", "to-do"])
                
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
            
    def get_issue_comments(self, issue_key: str) -> List[Dict[str, Any]]:
        """Busca a lista de comentários de um card no Jira Cloud."""
        if not self.is_configured:
            return []

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/comment"
        req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("comments", [])
        except Exception as e:
            print(f"[Jira Fetch Comments Error] {e}")
            return []

    def delete_comment(self, issue_key: str, comment_id: str) -> bool:
        """Apaga um comentário específico de um card no Jira Cloud."""
        if not self.is_configured:
            return True

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}/comment/{comment_id}"
        req = urllib.request.Request(url, headers=self._get_headers(), method="DELETE")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                return resp.status in (200, 204)
        except Exception as e:
            print(f"[Jira Delete Comment Error] {e}")
            return False

    def clear_all_comments(self, issue_key: str) -> bool:
        """Remove TODOS os comentários de um card em caso de não conformidade."""
        comments = self.get_issue_comments(issue_key)
        for c in comments:
            c_id = c.get("id")
            if c_id:
                self.delete_comment(issue_key, c_id)
        return True

    def get_issue_details(self, issue_key: str) -> Dict[str, Any]:
        """Obtém detalhes do card (incluindo parent, status, summary e campos)."""
        if not self.is_configured:
            return {}

        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue/{issue_key}?fields=summary,status,parent,comment"
        req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"[Jira Get Issue Details Error] {e}")
            return {}
