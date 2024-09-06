class Issue:
    def __init__(
        self,
        issue_type,
        issue_description,
        issue_element,
        issue_link,
        page_title,
        severity="low",
    ):
        self.issue_type = issue_type
        self.issue_description = issue_description
        self.issue_element = issue_element
        self.issue_link = issue_link
        self.issue_page_title = page_title
        self.severity = severity
