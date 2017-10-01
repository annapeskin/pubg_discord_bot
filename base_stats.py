from tabulate import tabulate
from operator import itemgetter

class Statistics:

    def __init__(self, title, default_str, headers=None):
        self.title = '---------===[ %s ]===---------' % title
        self.headers = headers
        self.list_of_stats = []
        self.default_str = default_str
        self.get_request_failed = None

    def __str__(self):
        if self.get_request_failed:
            return self.get_request_failed

        if not self.headers or not self.list_of_stats:
            return self.default_str

        self.list_of_stats = sorted(self.list_of_stats, key=(itemgetter(0)))  # TODO: improve this
        return '```\n%s\n%s\n```' % (self.title, tabulate(self.list_of_stats, headers=self.headers))

    def get_stats(self):
        raise NotImplementedError()
