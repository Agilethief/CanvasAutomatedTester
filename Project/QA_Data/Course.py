from .Assessment import Assessment
from .Module import Module
from .Page import Page

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
        self.pages = []
        self.assessments = []

    def set_title(self, newTitle: str):
        self.title = newTitle

    def set_url(self, newURL: str):
        self.url = newURL

    def set_participant_count(self, newCount: int):
        self.participant_count = newCount

    def set_page_count(self, newCount: int):
        self.page_count = newCount

    def set_module_count(self, newCount: int):
        self.module_count = newCount

    def set_assessment_count(self, newCount: int):
        self.assessment_count = newCount

    def set_link_count(self, newCount: int):
        self.link_count = newCount

    def set_image_count(self, newCount: int):
        self.image_count = newCount

    def get_page_count(self):  # TODO count these from elsewhere
        return self.page_count

    def get_link_count(self):  # TODO count these from elsewhere
        return self.link_count

    def get_image_count(self):  # TODO count these from elsewhere
        return self.image_count

    def get_participant_count(self):  # TODO count these from elsewhere
        return self.participant_count

    def set_modules(self, newModules: list[Module]):
        self.modules = newModules

    def set_pages(self, newPages: list):
        self.pages = newPages

    def set_assessments(self, newAssessments: list):
        self.assessments = newAssessments
