from typing import List, Union, Optional

from .newspaper import Newspaper
from .editor import Editor
from .subscriber import Subscriber



class Agency(object):
    singleton_instance = None

    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []

    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()

        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        for paper in self.newspapers:
            if paper.paper_id == new_paper.paper_id:
                return f'Newspaper with ID {new_paper.paper_id} already exists'
        self.newspapers.append(new_paper)

    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return 404

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)

    def add_editor(self, new_editor):
        for editor in self.editors:
            if editor.editor_id == new_editor.editor_id:
                return f'Editor with ID {new_editor.editor_id} already exists'
        self.editors.append(new_editor)


    def all_editors(self):
        return self.editors

    def get_editor(self, editor_id):
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return 404

    def remove_editor(self, editor):
        for edit in self.editors:
            for paper in editor.newspapers:
                if paper in edit.newspapers:
                    edit.issues.extend(editor.issues)
                    for issue in edit.issues:
                        issue.editor = edit
                        issue.editor_id = edit.editor_id
        self.editors.remove(editor)


    def editor_issues(self, editor):
        return editor.issues

    def add_subscriber(self, subscriber):
        for sub in self.subscribers:
            if sub.subscriber_id == subscriber.subscriber_id:
                return f'Subscriber with ID {subscriber.subscriber_id} already exists'
        self.subscribers.append(subscriber)

    def all_subscribers(self):
        return self.subscribers

    def get_subscriber(self, subscriber_id):
        for sub in self.subscribers:
            if sub.subscriber_id == subscriber_id:
                return sub
        return 404

    def remove_subscriber(self, subscriber):
        for p in subscriber.subscribes:
            p.subscribers.remove(subscriber)
        self.subscribers.remove(subscriber)


