import os
from typing import Dict, Any, List, Optional
import urllib.request
import urllib.parse
import json
import base64

class JiraConnector:
    """Connector for Jira Cloud API integration into FLOSE AEOS."""

    def __init__(self, domain: Optional[str] = None, email: Optional[str] = None, api_token: Optional[str] = None):
        self.domain = domain or os.environ.get("JIRA_DOMAIN", "")
        self.email = email or os.environ.get("JIRA_EMAIL", "")
        self.api_token = api_token or os.environ.get("JIRA_API_TOKEN", "")

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

    def create_issue(self, project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict[str, Any]:
        """Creates an Issue/Task in Jira."""
        if not self.is_configured:
            return {"mock": True, "message": "Jira connector running in simulation mode (credentials not set).", "summary": summary}
        
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
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}

    def search_issues(self, jql: str = "order by created DESC") -> List[Dict[str, Any]]:
        """Searches Jira issues via JQL."""
        if not self.is_configured:
            return [
                {"key": "FLO-101", "fields": {"summary": "Implement Auth Engine", "status": {"name": "In Progress"}}},
                {"key": "FLO-102", "fields": {"summary": "Setup MCP Jira Bridge", "status": {"name": "To Do"}}}
            ]
        
        url = f"https://{self.domain}.atlassian.net/rest/api/3/search?jql={urllib.parse.quote(jql)}"
        req = urllib.request.Request(url, headers=self._get_headers(), method="GET")
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("issues", [])
        except Exception as e:
            return [{"error": str(e)}]
