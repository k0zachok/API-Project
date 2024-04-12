import datetime
from .editor import Editor

class Issue(object):

    def __init__(self, issue_id, name, released: bool = False):
        self.issue_id = issue_id
        self.name = name
        self.releasedate = None
        self.released: bool = released


    def set_editor(self, editor):
        self.editor = editor
        self.editor_id = editor.editor_id
        editor.issues.append(self)
