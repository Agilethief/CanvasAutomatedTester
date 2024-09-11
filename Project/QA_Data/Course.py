from .Assessment import Assessment
from .Module import Module
from .Page import Page
from .Issue import Issue

# this script handles getting the top level course data
# - ID : int
# - Title : string
# - Participant count : int
# - Page count : int
# - Assessment count : int
# - link count : int
# - Image count : int
# - Modules[] : Module
# - Pages []: Page
# - Assessments[] : Assessment


class Course:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.url = ""
        self.participant_count = 0
        self.page_count = 0
        self.module_count = 0
        self.assessment_count = 0
        self.link_count = 0
        self.image_count = 0
        self.modules = []
        self.pages: list[Page] = []
        self.assessments: list[Assessment] = []
        self.issues: list[Issue] = []

    def get_total_word_count(self):
        word_count = 0
        for page in self.pages:
            word_count += page.word_count

        for ass in self.assessments:
            word_count += ass.word_count

        return word_count

    def get_total_link_count(self):
        link_count = 0
        for page in self.pages:
            link_count += page.link_count

        for ass in self.assessments:
            link_count += ass.link_count

        return link_count

    def get_total_image_count(self):
        img_count = 0
        for page in self.pages:
            img_count += page.image_count

        for ass in self.assessments:
            img_count += ass.image_count

        return img_count

    def get_page_and_assessment_count(self):
        return len(self.pages) + len(self.assessments)

    def get_avg_word_count(self):
        return self.get_avg_over_pages(self.get_total_word_count())

    def get_avg_link_count(self):
        return self.get_avg_over_pages(self.get_total_link_count())

    def get_avg_image_count(self):
        return self.get_avg_over_pages(self.get_total_image_count())

    def get_avg_over_pages(self, item_num):
        if item_num <= 0:
            return 0
        if self.get_page_and_assessment_count() <= 0:
            return

        return item_num / self.get_page_and_assessment_count()

    def create_issue(
        self, issue_type, issue_description, issue_element, issue_link, issue_page
    ):
        new_issue = Issue(
            issue_type, issue_description, issue_element, issue_link, issue_page
        )
        self.issues.append(new_issue)
