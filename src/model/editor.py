from typing import List

from flask_restx import Model

class Editor(object):
    def __init__(self, editor_id, name):
        self.editor_id = editor_id
        self.name = name
        self.issues = []