from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort
from ..model.issue import Issue
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.editor import Editor
import time


editor_ns = Namespace('editor', description='Editor related operations')

editor_model = editor_ns.model('Editor', {
    'name': fields.String,
    'address': fields.String
})


newspaper_nested_model = editor_ns.model('NewspaperNested',{
    'paper_id': fields.Integer,
    'name': fields.String
})

editor_get_model = editor_ns.model('EditorGet', {
    'editor_id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'newspapers': fields.List(fields.Nested(newspaper_nested_model), required=False)
})


@editor_ns.route('/')
class EditorAPI(Resource):
    @editor_ns.doc(editor_model, description='Create a new editor')
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        editor_id = int(str(time.time())[6:10])
        new_editor = Editor(editor_id=editor_id,
                            name=editor_ns.payload['name'],
                            address=editor_ns.payload['address'])
        create = Agency.get_instance().add_editor(new_editor)
        if create == 403:
            abort(403, f'Editor with ID {editor_id} already exists')
        else:
            create
        return new_editor

    @editor_ns.marshal_list_with(editor_get_model, envelope='editors')
    def get(self):
        return Agency.get_instance().all_editors()

@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
    @editor_ns.doc(editor_get_model, description="Get an editor's information")
    @editor_ns.marshal_with(editor_get_model, envelope='editor')
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if targeted_editor == 404:
            abort(404, f'Editor with ID {editor_id} was NOT found')
        return targeted_editor

    @editor_ns.doc(parser=editor_model, description="Update an editor's information")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='newspaper')
    def post(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if targeted_editor == 404:
            abort(404, f'Editor with ID {editor_id} was NOT found')
        targeted_editor.editor_id = editor_id
        targeted_editor.name = editor_ns.payload['name']
        targeted_editor.address = editor_ns.payload['address']
        return targeted_editor

    @editor_ns.doc(description='Delete an editor')
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if targeted_editor == 404:
            abort(404, f'Editor with ID {editor_id} was NOT found')
        Agency.get_instance().remove_editor(targeted_editor)
        return jsonify(f'Editor with ID {editor_id} was successfully removed')


editor_issues_model = editor_ns.model('EditorIssues', {
    'issue_id': fields.Integer,
    'name': fields.String,
    'pages': fields.Integer,
    'releasedate': fields.String(required=False),
    'released': fields.Boolean,
})

@editor_ns.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    @editor_ns.doc(editor_issues_model, description='Get a list of all issues made by editor')
    @editor_ns.marshal_with(editor_issues_model, envelope='editor')
    def get(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if targeted_editor == 404:
            abort(404, f'Editor with ID {editor_id} was NOT found')
        return Agency.get_instance().editor_issues(targeted_editor)