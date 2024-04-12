from ..src.model.agency import Agency
from ..src.model.newspaper import Newspaper
from ..src.model.editor import Editor
from ..src.model.subscriber import Subscriber


def create_newspapers(agency: Agency):
    paper1 = Newspaper(paper_id=100, name="The New York Times", frequency=7, price=13.14)
    paper2 = Newspaper(paper_id=101, name="Heute", frequency=1, price=1.12)
    paper3 = Newspaper(paper_id=115, name="Wall Street Journal", frequency=1, price=3.00)
    paper4 = Newspaper(paper_id=125, name="National Geographic", frequency=30, price=34.00)
    agency.newspapers.extend([paper1, paper2, paper3, paper4])


def create_editors(agency: Agency):
    editor1 = Editor(editor_id=123, name='Robert', address='Krems')
    editor2 = Editor(editor_id=457, name='Joe', address='Vienna')
    editor3 = Editor(editor_id=923, name='Harvey', address='Kyiv')
    agency.editors.extend([editor1,editor2,editor3])

def create_subscriber(agency: Agency):
    sub1 = Subscriber(subscriber_id=356, name='Ronnie', address='London')
    sub2 = Subscriber(subscriber_id=765, name='John', address='Eindhoven')
    sub3 = Subscriber(subscriber_id=915, name='Franklin', address='Cologne')
    agency.subscribers.extend([sub1, sub2, sub3])

def populate(agency: Agency):
    create_newspapers(agency)
    create_editors(agency)
    create_subscriber(agency)