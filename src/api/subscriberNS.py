from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields, abort
from ..model.issue import Issue
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.editor import Editor
from ..model.subscriber import Subscriber
import time

subscriber_ns = Namespace('subscriber', description='Subscriber related operations')

subscriber_model = subscriber_ns.model('Subscriber', {
    'name': fields.String,
    'address': fields.String
})

subscriber_get_model = subscriber_ns.model('SubscriberGet', {
    'subscriber_id': fields.Integer,
    'name': fields.String,
    'address': fields.String
})

@subscriber_ns.route('/')
class SubscriberAPI(Resource):
    @subscriber_ns.doc(subscriber_model, description='Create a new subscriber')
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        subscriber_id = int(str(time.time())[6:10])
        new_subscriber = Subscriber(subscriber_id=subscriber_id,
                                    name=subscriber_ns.payload['name'],
                                    address=subscriber_ns.payload['address'])
        Agency.get_instance().add_subscriber(new_subscriber)
        return new_subscriber

    @subscriber_ns.doc(subscriber_get_model, description='List all subscribers')
    @subscriber_ns.marshal_with(subscriber_get_model, envelope='subscribers')
    def get(self):
        return Agency.get_instance().all_subscribers()

sub_newspaper_model = subscriber_ns.model('Subs', {
    'paper_id': fields.Integer,
    'name': fields.String
})

issues_model = subscriber_ns.model('Issues', {
    'issue_id': fields.Integer,
    'name': fields.String
})

subscriber_info_model = subscriber_ns.model('SubInfoModel', {
    'subscriber_id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'subscribes': fields.List(fields.Nested(sub_newspaper_model), required=False),
    'issues': fields.List(fields.Nested(issues_model), required=False)
})

@subscriber_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource):
    @subscriber_ns.doc(subscriber_info_model, description="Get a subscribers information")
    @subscriber_ns.marshal_with(subscriber_info_model, envelope='subscriber')
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if targeted_subscriber == 404:
            abort(404, f'Subscriber with ID {subscriber_id} was NOT found')
        return targeted_subscriber

    @subscriber_ns.doc(parser=subscriber_model, description="Update a subscriber's information")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if targeted_subscriber == 404:
            abort(404, f'Subscriber with ID {subscriber_id} was NOT found')
        targeted_subscriber.subscriber_id = subscriber_id
        targeted_subscriber.name = subscriber_ns.payload['name']
        return targeted_subscriber

    @subscriber_ns.doc(description='Delete a subscriber')
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if targeted_subscriber == 404:
            abort(404, f'Subscriber with ID {subscriber_id} was NOT found')
        Agency.get_instance().remove_subscriber(targeted_subscriber)
        return jsonify(f'Subscriber with ID {subscriber_id} was successfully removed')


subscribe_model = subscriber_ns.model('SubscribeModel', {
    'paper_id': fields.Integer
})

@subscriber_ns.route('/<int:subscriber_id>/subscribe')
class Subscribe(Resource):
    @subscriber_ns.doc(subscribe_model, description='Subscribe on Newspaper')
    @subscriber_ns.expect(subscribe_model, validate=True)
    @subscriber_ns.marshal_with(subscribe_model, envelope='Subscribe')
    def post(self, subscriber_id):
        targeted_paper = Agency.get_instance().get_newspaper(subscriber_ns.payload['paper_id'])
        if targeted_paper == 404:
            abort(404, f'Newspaper with ID {subscriber_ns.payload["paper_id"]} was NOT found')
        Agency.get_instance().get_subscriber(subscriber_id).subscribe(targeted_paper)
        return targeted_paper

subscriber_stats_model = subscriber_ns.model('SubStats', {
    'subscriber_id': fields.Integer,
    'name': fields.String,
    'monthly_cost': fields.Integer,
    'annual_cost': fields.Integer,
    'number_of_issues': fields.Integer
})

@subscriber_ns.route('/<int:subscriber_id>/stats')
class SubscriberStats(Resource):
    #TODO: display issues specifically for paper (make a function that returns a dict and use it instead of marshal with) HOW TO IMPLEMENT BOTH DICT AND MODEL WITH OTHER INFO
    @subscriber_ns.doc(subscriber_stats_model, description="Subscriber's Statistics")
    @subscriber_ns.marshal_with(subscriber_stats_model, envelope='substats')
    def get(self, subscriber_id):
        targeted_sub = Agency.get_instance().get_subscriber(subscriber_id)
        if targeted_sub == 404:
            abort(404, f'Subscriber with ID {subscriber_id} was NOT found')
        targeted_sub.monthly()
        targeted_sub.annual()
        targeted_sub.num_issues()
        return targeted_sub


miss_issue_model = subscriber_ns.model('MissIssue', {
    'issue_id':fields.Integer,
    'name':fields.String
})

missing_issues_model = subscriber_ns.model('MissingIssues',{
    'missing_issues':fields.List(fields.Nested(miss_issue_model), required=False)
})

@subscriber_ns.route('/<int:subscriber_id>/missingissues')
class MissingIssues(Resource):
    @subscriber_ns.doc(missing_issues_model, description='Get issues that were not delivered to subscribers')
    @subscriber_ns.marshal_with(missing_issues_model, envelope='missing issues')
    def get(self, subscriber_id):
        targeted_sub = Agency.get_instance().get_instance().get_subscriber(subscriber_id)
        if targeted_sub == 404:
            abort(404, f'Subscriber with ID {subscriber_id} was NOT found')
        targeted_sub.miss_issues()
        if len(targeted_sub.missing_issues) == 0:
            abort(404, f'There is no missing issues for Subscriber {subscriber_id}')
        return targeted_sub
