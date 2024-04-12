from .newspaper import Newspaper


class Subscriber(object):
    def __init__(self, subscriber_id, name, address):
        self.subscriber_id = subscriber_id
        self.name = name
        self.address = address
        self.subscribes = []
        self.issues = []
        self.subs_num = len(self.subscribes)
        self.missing_issues = []



    def subscribe(self, newspaper):
        self.subscribes.append(newspaper)
        newspaper.subscribers.append(self)

    def monthly(self):
        self.monthly_cost = 0
        for sub in self.subscribes:
            self.monthly_cost += (30 // sub.frequency) * sub.price
        return self.monthly_cost

    def annual(self):
        self.annual_cost = self.monthly_cost * 12


    def num_issues(self):
        self.number_of_issues = len(self.issues)

    def miss_issues(self):
        for p in self.subscribes:
            for i in p.issues:
                if i.released and i not in self.issues and i not in self.missing_issues:
                    self.missing_issues.append(i)








