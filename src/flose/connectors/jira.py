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
    """Connector for REAL Jira Cloud API with Comments & Issue Creation."""

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

    def fetch_real_jira_issues(self, project_key: str = "KAN", limit: int = 10) -> List[Dict[str, Any]]:
        """Busca os cards REAIS e seus comentários diretamente no Jira Cloud."""
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
                                "status": d_data.get("fields", {}).get("status", {}).get("name", "In Progress"),
                                "type": "Card Real Jira",
                                "comments": comments
                            })
                    except Exception:
                        continue
        except Exception as e:
            print(f"[Jira Fetch Error] {e}")
            
        return issues_result

    def add_comment(self, issue_key: str, author_name: str, comment_text: str) -> Dict[str, Any]:
        """Adiciona um comentário real do agente (Felipe, Sofia, Lucas, Beatriz) na issue do Jira."""
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

    def create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        if not self.is_configured:
            return {"mock": True, "summary": summary}
        
        url = f"https://{self.domain}.atlassian.net/rest/api/3/issue"
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}]
                    }]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=self._get_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}
