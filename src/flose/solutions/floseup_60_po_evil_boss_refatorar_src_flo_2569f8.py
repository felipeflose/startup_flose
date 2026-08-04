from typing import Dict, Optional

class JiraConnector:
    def fetch_data(self, issue_id: str) -> Dict[str, Optional[str]]:
        try:
            # Simulação de chamada à API Jira
            data = {'id': issue_id, 'summary': 'Issue Title', 'description': None}
            return data
        except Exception as e:
            raise ConnectionError(f'Erro ao buscar dados do Jira: {e}')
