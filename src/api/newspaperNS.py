from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from ..model.issue import Issue
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.editor import Editor
import time
import datetime

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

paper_model = newspaper_ns.model('NewspaperModel', {
    # 'paper_id': fields.Integer(required=False,
    #         help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
                          help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
                                help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
                          help='The monthly price of the newspaper (e.g. 12.3)')
})

subscriber_get_model = newspaper_ns.model('SubscriberGet', {
    'subscriber_id': fields.Integer,
    'name': fields.String
})

paper_get_model = newspaper_ns.model('NewspaperGet', {
    'paper_id': fields.Integer(required=False,
                               help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
                          help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
                                help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
                          help='The monthly price of the newspaper (e.g. 12.3)'),
    'subscribers': fields.List(fields.Nested(subscriber_get_model), required=False),
})


@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        paper_id = int(str(time.time())[6:10])
        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)
        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_get_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(parser=paper_model, description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        # print(newspaper_ns.payload)
        targeted_paper.name = newspaper_ns.payload['name']
        targeted_paper.frequency = newspaper_ns.payload['frequency']
        targeted_paper.price = newspaper_ns.payload['price']
        return targeted_paper

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")


issue_model = newspaper_ns.model('Issue', {
    'name': fields.String,
    'pages': fields.Integer
})

issue_get_model = newspaper_ns.model('IssueGet', {
    'issue_id': fields.Integer,
    'name': fields.String,
    'pages': fields.Integer,
    'releasedate': fields.String(required=False),
    'released': fields.Boolean,
    'editor_id': fields.Integer
})


@newspaper_ns.route('/<int:paper_id>/issue')
class IssueAPI(Resource):
    @newspaper_ns.doc(issue_model, description="Add a new issue")
    @newspaper_ns.expect(issue_model, validate=True)
    @newspaper_ns.marshal_with(issue_model, envelope='newspaper')
    def post(self, paper_id):
        issue_id = int(str(time.time())[5:10])
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify('The following paper was NOT found')
        new_issue = Issue(issue_id=issue_id,
                          name=newspaper_ns.payload['name'],
                          pages=newspaper_ns.payload['pages'],
                          newspaper=targeted_paper,
                          released=False)
        targeted_paper.add_issue(new_issue)
        return new_issue

    @newspaper_ns.doc(issue_model, description='List all issues of a specific newspaper')
    @newspaper_ns.marshal_with(issue_get_model)
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify('The following paper was NOT found')
        return targeted_paper.all_issues()


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class IssueID(Resource):
    @newspaper_ns.doc(issue_model, description='Get info of a newspaper issue')
    @newspaper_ns.marshal_with(issue_model, envelope='newspaper')
    def get(self, paper_id, issue_id):
        targeted_newspaper = Agency.get_instance().get_newspaper(paper_id)
        targeted_issue = targeted_newspaper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify('The following issue was NOT found')
        return targeted_issue


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class IssueRelease(Resource):
    @newspaper_ns.doc(issue_model, description='Release an issue')
    @newspaper_ns.marshal_with(issue_model, envelope='newspaper')
    def post(self, paper_id, issue_id):
        targeted_newspaper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_newspaper:
            return jsonify('The following newspaper was NOT found')
        targeted_issue = targeted_newspaper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify('The following issue was NOT found')
        targeted_issue.releasedate = datetime.date.today()
        targeted_newspaper.release_issue(issue_id)
        return targeted_issue


issue_editor_model = newspaper_ns.model('IssueEditor', {
    "editor_id": fields.Integer
})


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class IssueEditor(Resource):
    @newspaper_ns.doc(issue_editor_model, description='Specify an editor')
    @newspaper_ns.expect(issue_editor_model, validate=True)
    @newspaper_ns.marshal_with(issue_editor_model, envelope='IssueEditor')
    def post(self, paper_id, issue_id):
        editor_id = newspaper_ns.payload['editor_id']
        targeted_newspaper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_newspaper:
            return jsonify('The following newspaper was NOT found')
        targeted_issue = targeted_newspaper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify('The following issue was NOT found')
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f'Editor with ID {editor_id} was NOT found')
        targeted_issue.set_editor(targeted_editor)
        return f'Editor {targeted_editor} set for the issue {targeted_issue}'


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/deliver')
class IssueDeliver(Resource):
    def post(self, paper_id, issue_id):
        targeted_newspaper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_newspaper:
            return jsonify('The following newspaper was NOT found')
        targeted_issue = targeted_newspaper.get_issue(issue_id)
        if not targeted_issue:
            return jsonify('The following issue was NOT found')
        if targeted_issue.released:
            for sub in Agency.get_instance().all_subscribers():
                if targeted_newspaper in sub.subscribes:
                    sub.issues.append(targeted_issue)
                    return jsonify(f'Issue {targeted_issue.issue_id} was delivered SUCCESSFULLY')
        else:
            return jsonify(f'Issue with ID {targeted_issue.issue_id} was NOT released yet')


newspaper_statistics_model = newspaper_ns.model('NewspaperStats', {
    'paper_id': fields.Integer,
    'name': fields.String,
    'number_of_subscribers': fields.Integer,
    'monthly_revenue': fields.Integer,
    'annual_revenue': fields.Integer
})

@newspaper_ns.route('/<int:paper_id>/stats')
class NewspaperStats(Resource):
    @newspaper_ns.doc(newspaper_statistics_model, description='Get statistics of Newspaper')
    @newspaper_ns.marshal_with(newspaper_statistics_model, envelope='newspaper stats')
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f'Newspaper with ID {paper_id} was NOT found')
        targeted_paper.monthly()
        targeted_paper.annual()
        targeted_paper.num_subs()
        return targeted_paper
