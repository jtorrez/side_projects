from bs4 import BeautifulSoup
from pymongo import MongoClient

class HTMLParser(object):
    def __init__(self):
        self.client = MongoClient()
        self.soup = None
        self.html = None

    def load_html(self, db_name, coll_name, find_term, find_cond):
        db = self.client[db_name]
        coll = db[coll_name]
        cursor = coll.find({find_term: find_cond})
        self.html = cursor[0]['html']

    def _build_soup(self, parser):
        self.soup = BeautifulSoup(self.html, parser)

    def parse_html(self, css_selector, parser='html.parser'):
        if not self.soup:
            self._build_soup(parser)
        results = self.soup.select(css_selector)
        return results

class TrumpParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.question_ids = []
        self.yes_no_list = yes_no_list = [False,
                                          True,
                                          True,
                                          False,
                                          None,
                                          None,
                                          True,
                                          False,
                                          False,
                                          True,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False,
                                          False]

    def _parse_question_ids(self):
        survey_questions = self.parse_html('li.q-item')
        for question in survey_questions:
            question_section = question.select('ul')
            if question_section:
                self.question_ids.append(question_section[0]['id'][3:])

    def get_button_question_lists(self):
        self._parse_question_ids()
        yes_questions = []
        no_questions = []

        for yes, question_id in zip(self.yes_no_list, self.question_ids):
            if yes == None:
                continue
            elif yes:
                yes_questions.append("{}".format(question_id))
            else:
                no_questions.append("{}".format(question_id))
        return yes_questions, no_questions
