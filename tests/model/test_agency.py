import pytest

from ...src.model.newspaper import Newspaper
from ...src.model.editor import Editor
from ...src.model.subscriber import Subscriber
from ..fixtures import app, client, agency


def test_add_newspaper(agency):
    before = len(agency.newspapers)
    new_paper = Newspaper(paper_id=999,
                          name="Simpsons Comic",
                          frequency=7,
                          price=3.14)
    agency.add_newspaper(new_paper)
    assert len(agency.all_newspapers()) == before + 1


# def test_add_newspaper_same_id_should_raise_error(agency):
#     before = len(agency.newspapers)
#     new_paper = Newspaper(paper_id=999,
#                           name="Simpsons Comic",
#                           frequency=7,
#                           price=3.14)
#
#     # first adding of newspaper should be okay
#     agency.add_newspaper(new_paper)
#
#     new_paper2 = Newspaper(paper_id=999,
#                           name="Superman Comic",
#                           frequency=7,
#                           price=13.14)
#
#     with pytest.raises(ValueError, match='A newspaper with ID 999 already exists'):  # <-- this allows us to test for exceptions
#         # this one should rais ean exception!
#         agency.add_newspaper(new_paper2)
#         assert ValueError



def test_get_newspaper(agency):
    paper = agency.get_newspaper(100)
    assert paper.paper_id == 100
    assert paper.name == 'The New York Times'
    assert paper.frequency == 7
    assert paper.price == 13.14

def test_all_newspapers(agency):
    assert agency.newspapers == agency.all_newspapers()

def test_remove_newspaper(agency):
    before = len(agency.all_newspapers())
    targeted_newspaper = agency.get_instance().get_newspaper(101)
    agency.remove_newspaper(targeted_newspaper)

    assert len(agency.all_newspapers()) == before - 1


def test_add_editor(agency):
    before = len(agency.editors)
    new_editor = Editor(editor_id=1,
                        name='Editor Name',
                        address='Berlin')
    agency.add_editor(new_editor)

    assert before + 1 == len(agency.all_editors())

def test_remove_editor(agency):
    before = len(agency.editors)
    targeted_editor = agency.get_instance().get_editor(123)
    agency.remove_editor(targeted_editor)
    assert len(agency.all_editors()) == before - 1


def test_all_editors(agency):
    assert agency.editors == agency.all_editors()
def test_add_subscriber(agency):
    before = len(agency.editors)
    new_editor = Subscriber(subscriber_id=2,
                        name='Jimmy',
                        address='Rome')
    agency.add_subscriber(new_editor)
    assert len(agency.subscribers) == before + 1

    # def test_add_subscriber_for_same_id(agency):
    #     new_subscriber1 = Subscriber(subscriber_id=3,
    #                             name='Jimmy')
    #     agency.add_subscriber(new_subscriber1)
    #
    #     new_subscriber2 = Subscriber(subscriber_id=3,
    #                             name='Ronald')
    #
    #     agency.add_subscriber(new_subscriber2)

def test_all_subscribers(agency):
    assert agency.subscribers == agency.all_subscribers()
def test_get_subscriber(agency):
    targeted_subscriber = agency.get_subscriber(765)
    assert targeted_subscriber.subscriber_id == 765
    assert targeted_subscriber.name == 'John'

def test_remove_subscriber(agency):
    before = len(agency.subscribers)
    targeted_subscriber = agency.get_subscriber(915)
    agency.remove_subscriber(targeted_subscriber)
    assert len(agency.subscribers) == before - 1
