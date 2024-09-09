class Assessment:

    def __init__(self, id, title, course):
        self.id = id
        self.title = title
        self.url = ""
        self.assessment_type = ""
        self.points = 0
        self.group = ""
        self.mark_display = ""
        self.grading_scheme = ""
        self.due_date = ""
        self.release_date = ""
        self.build_on_last_attempt = "Enabled"
        self.mark_release_policy = "Manual"
        self.published = False
        self.issue_count = 0
        self.course = course
        self.word_count = 0
        self.link_count = 0
        self.image_count = 0
        self.question_count = 0

    def create_issue(self, issue_type, issue_description, issue_element):
        self.issue_count += 1
        self.course.create_issue(
            issue_type, issue_description, issue_element, self.url, self.title
        )

    def print_stats(self):
        print("ID:", self.id)
        print("Title:", self.title)
        print("URL:", self.url)
        print("Assessment Type:", self.assessment_type)
        print("Points:", self.points)
        print("Group:", self.group)
        print("Mark Display:", self.mark_display)
        print("Grading Scheme:", self.grading_scheme)
        print("Due Date:", self.due_date)
        print("Release Date:", self.release_date)
        print("Build on Last Attempt:", self.build_on_last_attempt)
        print("Mark Release Policy:", self.mark_release_policy)
        print("Published:", self.published)
        print("Issue Count:", self.issue_count)
