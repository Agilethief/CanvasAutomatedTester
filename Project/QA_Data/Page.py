from .I_Statable import I_Statable


class Page(I_Statable):

    def __init__(self, url, course):
        self.url = url
        self.title = "page"
        self.link_count = 0
        self.links = []
        self.word_count = 0
        self.image_count = 0
        self.course = course
        self.module = ""
        self.issue_count = 0
        self.published = False

    def create_issue(
        self, issue_type, issue_description, issue_element, issue_link, issue_page
    ):
        self.issue_count += 1
        self.course.create_issue(
            issue_type, issue_description, issue_element, issue_link, issue_page
        )

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_published(self):
        return self.published

    def get_issue_count(self):
        return self.issue_count

    def get_course(self):
        return self.course

    def get_word_count(self):
        return self.word_count

    def get_link_count(self):
        return self.link_count

    def get_image_count(self):
        return self.image_count
