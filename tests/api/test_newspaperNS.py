# import the fixtures (this is necessary!)
from ..fixtures import app, client, agency

def test_get_newspaper_should_list_all_papers(client, agency):
    # send request
    response = client.get("/newspaper/")   # <-- note the slash at the end!

    # test status code
    assert response.status_code == 200

    # parse response and check that the correct data is here
    parsed = response.get_json()
    assert len(parsed["newspapers"]) == len(agency.newspapers)


def test_add_newspaper(client, agency):
    # prepare
    paper_count_before = len(agency.newspapers)

    # act
    response = client.post("/newspaper/",  # <-- note the slash at the end!
                           json={
                               "name": "Simpsons Comic",
                               "frequency": 7,
                               "price": 3.14
                           })
    assert response.status_code == 200
    # verify

    assert len(agency.newspapers) == paper_count_before + 1
    # parse response and check that the correct data is here
    parsed = response.get_json()
    paper_response = parsed["newspaper"]

    # verify that the response contains the newspaper data
    assert paper_response["name"] == "Simpsons Comic"
    assert paper_response["frequency"] == 7
    assert paper_response["price"] == 3.14


def test_get_newspaper_by_id(client, agency):
    response = client.get('/newspaper/101')

    assert response.status_code == 200
    paper = response.get_json()['newspaper']
    assert paper['name'] == 'Heute'
    assert paper['frequency'] == 1
    assert paper['price'] == 1.12


def test_update_newspaper(client, agency):
    before = len(agency.newspapers)
    response = client.post('/newspaper/115',
                           json={
                               'name': 'TestGazeta',
                               'frequency': 7,
                               'price': 1.15
                           })

    assert response.status_code == 200
    assert len(agency.newspapers) == before
    targeted_paper = agency.get_newspaper(115)
    assert targeted_paper.name == 'TestGazeta'
    assert targeted_paper.frequency == 7
    assert targeted_paper.price == 1.15

def test_delete_newspaper(client,agency):
    before = len(agency.newspapers)
    response = client.delete('/newspaper/125')
    assert response.status_code == 200
    assert len(agency.newspapers) == before - 1


def test_post_issue(client, agency):
    paper = agency.get_newspaper(115)
    before = len(paper.issues)
    response = client.post('/newspaper/115/issue',
                           json={
                               'name': 'TestIssue',
                               'pages': 20
                           })
    assert response.status_code == 200
    assert len(paper.issues) == before + 1
    issue = paper.issues[len(paper.issues)-1]
    assert issue.name == 'TestIssue'
    assert issue.pages == 20

def test_all_issues(client, agency):
    response = client.get('/newspaper/115/issue')
    assert response.status_code == 200

    issues = response.get_json()
    print(issues)
    paper = agency.get_newspaper(115)
    assert len(issues) == len(paper.issues)


def test_get_issue_by_id(client, agency):
    response = client.get('/newspaper/100/issue/777')
    assert response.status_code == 200

    issue = response.get_json()['newspaper']
    assert issue['name'] == 'NYTimes2'
    assert issue['pages'] == 16

def test_issue_release(client,agency):
    paper = agency.get_newspaper(100)
    issue = paper.get_issue(777)
    assert not issue.released
    response = client.post('/newspaper/100/issue/777/release')
    assert issue.released

def test_set_editor(client, agency):
    response = client.post('/newspaper/100/issue/777/editor')
    targeted_paper = agency.get_newspaper(100)
    targeted_issue = targeted_paper.get_issue(777)
    targeted_editor = agency.get_editor(123)
    before_issues = len(targeted_editor.issues)
    targeted_issue.set_editor(targeted_editor)
    assert targeted_issue.editor == targeted_editor
    assert targeted_issue.editor_id == targeted_editor.editor_id
    assert len(targeted_editor.issues) == before_issues + 1

def test_deliver_issue_to_subscriber(client, agency):
    response = client.post('/newspaper/100/issue/777/deliver')
    targeted_subscriber = agency.get_subscriber(356)
    targeted_newspaper = agency.get_newspaper(100)
    before_sub = len(targeted_subscriber.subscribes)
    before_pap = len(targeted_newspaper.subscribers)
    targeted_subscriber.subscribe(targeted_newspaper)
    assert len(targeted_subscriber.subscribes) == before_sub + 1
    assert len(targeted_newspaper.subscribers) == before_pap + 1



