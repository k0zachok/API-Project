from ..fixtures import app, client, agency

def test_add_editor(client, agency):
    before = len(agency.editors)
    response = client.post('/editor/',
                           json={
                               'name': 'Emilia',
                               'address': 'Barcelona'
                           })
    assert response.status_code == 200
    assert len(agency.editors) == before + 1
    parsed = response.get_json()
    editor_response = parsed['editor']
    assert editor_response['name'] == 'Emilia'
    assert editor_response['address'] == 'Barcelona'


def test_get_all_editors(client, agency):
    response = client.get('/editor/')

    assert response.status_code == 200

    parsed = response.get_json()
    assert len(parsed['editors']) == len(agency.editors)

def test_get_editor_by_id(client, agency):
    response = client.get('/editor/457')
    assert response.status_code == 200
    parsed = response.get_json()['editor']
    assert parsed['editor_id'] == 457
    assert parsed['name'] == 'Joe'
    assert parsed['address'] == 'Vienna'


def test_update_editor(client, agency):
    targeted_editor = agency.get_editor(923)
    assert targeted_editor.editor_id == 923
    assert targeted_editor.name == 'Harvey'
    assert targeted_editor.address == 'Kyiv'
    before = len(agency.editors)
    response = client.post('/editor/923',
                           json={
                               'name': 'Andrew',
                               'address': 'Prague'
                           })
    assert response.status_code == 200
    assert len(agency.editors) == before
    targeted_editor = agency.get_editor(923)
    assert targeted_editor.editor_id == 923
    assert targeted_editor.name == 'Andrew'
    assert targeted_editor.address == 'Prague'

def test_delete_editor(client, agency):
    before = len(agency.editors)
    response = client.delete('/editor/923')
    assert response.status_code == 200
    assert len(agency.editors) == before - 1

def test_get_issues_of_editor(client, agency):
    response = client.get('/editor/457/issues')
    assert response.status_code == 200
    parsed = response.get_json()['editor']
    targeted_editor = agency.get_editor(457)
    assert len(agency.editor_issues(targeted_editor)) == len(parsed)

