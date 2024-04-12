from typing import List

from flask_restx import Model

class Editor(object):
    def __init__(self, editor_id, name, address):
        self.editor_id = editor_id
        self.name = name
        self.address = address
        self.issues = []
        self.newspapers = []