from flose.solutions.floseup_205_po_evil_boss_refatorar_src_flo_b712bb import fetch_issues, handle_jira_exception

def test_fetch_issues_connection_error(mocker):
    mocker.patch('flose.connectors.jira.requests.get', side_effect=ConnectionError)
    with pytest.raises(SystemExit) as excinfo:
        fetch_issues()
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1

def test_fetch_issues_http_error(mocker):
    mocker.patch('flose.connectors.jira.requests.get', side_effect=HTTPError)
    with pytest.raises(SystemExit) as excinfo:
        fetch_issues()
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1

def test_fetch_issues_timeout_error(mocker):
    mocker.patch('flose.connectors.jira.requests.get', side_effect=Timeout)
    with pytest.raises(SystemExit) as excinfo:
        fetch_issues()
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1

def test_fetch_issues_unhandled_exception(mocker, caplog):
    mocker.patch('flose.connectors.jira.requests.get', side_effect=Exception)
    with pytest.raises(SystemExit) as excinfo:
        fetch_issues()
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1
    assert 'Exceção não tratada' in caplog.text