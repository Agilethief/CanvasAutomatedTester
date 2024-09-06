class Page:

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
