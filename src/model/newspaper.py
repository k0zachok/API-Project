from typing import List

from flask_restx import Model

from .issue import Issue


class Newspaper(object):


    def __init__(self, paper_id: int, name: str, frequency: int, price: float):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency: int = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
        self.subscribers = []

    def add_issue(self, new_issue: Issue):
        self.issues.append(new_issue)

    def all_issues(self):
        return self.issues

    def get_issue(self, issue_id):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None

    def release_issue(self, issue_id):
        for issue in self.issues:
            if issue.issue_id == issue_id:
                issue.released = True

    def num_subs(self):
        self.number_of_subscribers = len(self.subscribers)

    def monthly(self):
        self.montly_revenue = ((30 // self.frequency) * self.price) * len(self.subscribers)

    def annual(self):
        self.annual_revenue = self.montly_revenue * 12