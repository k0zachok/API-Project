from ..fixtures import app, client, agency

def test_add_subscriber(client, agency):
    before = len(agency.subscribers)
    response = client.post('/subscriber/',
                           json={
                           'name': 'Bruce',
                           'address': 'Los Angeles'
                           })
    assert response.status_code == 200
    assert len(agency.subscribers) == before + 1
    parsed = response.get_json()['subscriber']
    assert parsed['name'] == 'Bruce'
    assert parsed['address'] == 'Los Angeles'

def test_get_all_subscribers(client, agency):
    response = client.get('/subscriber/')
    assert response.status_code == 200
    parsed = response.get_json()['subscribers']
    assert len(parsed) == len(agency.subscribers)

def test_get_subscriber_by_id(client, agency):
    response = client.get('/subscriber/915')
    response1 = client.get('/subscriber/000')
    assert response1.status_code == 404
    assert response.status_code == 200
    targeted_sub = agency.get_subscriber(915)
    parsed = response.get_json()['subscriber']
    assert targeted_sub.subscriber_id == parsed['subscriber_id']
    assert targeted_sub.name == parsed['name']
    assert targeted_sub.address == parsed['address']

def test_update_subscriber(client, agency):
    before = len(agency.subscribers)
    targeted_subscriber = agency.get_subscriber(356)
    assert targeted_subscriber.subscriber_id == 356
    assert targeted_subscriber.name == 'Ronnie'
    assert targeted_subscriber.address == 'London'
    response = client.post('/subscriber/356',
                           json={
                               'name': 'David',
                               'address': 'Burgas'
                           })
    response1 = client.post('/subscriber/000',
                            json={
                                'name': 'David',
                                'address': 'Burgas'
                            })
    assert response1.status_code == 404
    assert response.status_code == 200
    assert len(agency.subscribers) == before
    targeted_subscriber = agency.get_subscriber(356)
    assert targeted_subscriber.subscriber_id == 356
    assert targeted_subscriber.name == 'David'
    assert targeted_subscriber.address == 'Burgas'

def test_delete_subscriber(client, agency):
    before = len(agency.subscribers)
    response = client.delete('/subscriber/765')
    response1 = client.delete('/subscriber/000')
    assert response1.status_code == 404
    assert response.status_code == 200
    assert len(agency.subscribers) == before - 1

def test_subscribe(client, agency):
    response = client.post('/subscriber/356/subscribe',
                           json={
                               'paper_id':100
                           })
    response1 = client.post('/subscriber/000/subscribe',
                            json={
                                'paper_id':100
                            })
    response2 = client.post('/subscriber/356/subscribe',
                            json={
                                'paper_id':000
                            })
    assert response1.status_code == 404
    assert response2.status_code == 404
    parsed = response.get_json()
    targeted_subscriber = agency.get_subscriber(765)
    targeted_newspaper = agency.get_newspaper(100)
    before_subscribes = len(targeted_subscriber.subscribes)
    before_subscribers = len(targeted_newspaper.subscribers)
    targeted_subscriber.subscribe(targeted_newspaper)
    assert len(targeted_subscriber.subscribes) == before_subscribes + 1
    assert len(targeted_newspaper.subscribers) == before_subscribers + 1


def test_subscriber_missing_issues(client, agency):
    targeted_subscriber = agency.get_subscriber(915)
    targeted_newspaper = agency.get_newspaper(100)
    targeted_issue = targeted_newspaper.get_issue(777)
    targeted_subscriber.subscribe(targeted_newspaper)
    response = client.get('/subscriber/915/missingissues')
    assert response.status_code == 200
    parsed = response.get_json()['missing issues']['missing_issues'][0]
    assert parsed['issue_id'] == 777
    assert parsed['name'] == 'NYTimes2'