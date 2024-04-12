from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from ..model.issue import Issue
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.editor import Editor
import time


editor_ns = Namespace('editor', description='Editor related operations')

editor_model = editor_ns.model('Editor', {
    'editor_id': fields.Integer,
    'name': fields.String,
})


@editor_ns.route('/')
class EditorAPI(Resource):
    @editor_ns.doc(editor_model, description='Create a new editor')
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        editor_id = int(str(time.time())[7:10])
        new_editor = Editor(editor_id=editor_id,
                            name=editor_ns.payload['name'])
        Agency.get_instance().add_editor(new_editor)
        return new_editor

    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return Agency.get_instance().all_editors()

@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
    @editor_ns.doc(editor_model, description="Get an editor's information")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return 'The following editor was NOT found'
        return targeted_editor

    @editor_ns.doc(parser=editor_model, description="Update an editor's information")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='newspaper')
    def post(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        targeted_editor.editor_id = editor_id
        targeted_editor.name = editor_ns.payload['name']
        return targeted_editor

    @editor_ns.doc(description='Delete an editor')
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return f'Editor with ID {editor_id} was NOT found'
        Agency.get_instance().remove_editor(targeted_editor)
        return f'Editor with ID {editor_id} was successfully removed'


editor_issues_model = editor_ns.model('EditorIssues', {
    'issue_id': fields.Integer,
    'name': fields.String,
    'releasedate': fields.String(required=False),
    'released': fields.Boolean,
})

@editor_ns.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    @editor_ns.doc(editor_issues_model, description='Get a list of all issues made by editor')
    @editor_ns.marshal_with(editor_issues_model, envelope='editor')
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        return Agency.get_instance().editor_issues(targeted_editor)