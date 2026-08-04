import pytest
from flose.solutions.floseup_68_po_evil_boss_refatorar_src_flo_a2fbd8 import *

@pytest.fixture
def jira_connector():
    return JiraConnector()

def test_fetch_data(jira_connector):
    data = jira_connector.fetch_data()
    assert isinstance(data, dict)
