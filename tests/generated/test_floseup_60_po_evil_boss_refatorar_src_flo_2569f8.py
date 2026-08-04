from flose.solutions.floseup_60_po_evil_boss_refatorar_src_flo_2569f8 import *
import pytest

@pytest.mark.parametrize('issue_id, expected', [
    ('12345', {'id': '12345', 'summary': 'Issue Title', 'description': None}),
    ('67890', {'id': '67890', 'summary': None, 'description': None})
])
def test_fetch_data(issue_id, expected):
    connector = JiraConnector()
    result = connector.fetch_data(issue_id)
    assert result == expected

def test_fetch_data_exception(mocker):
    mocker.patch.object(JiraConnector, 'fetch_data', side_effect=Exception('API Error'))
    with pytest.raises(ConnectionError) as e:
        JiraConnector().fetch_data('12345')
    assert str(e.value) == 'Erro ao buscar dados do Jira: API Error'