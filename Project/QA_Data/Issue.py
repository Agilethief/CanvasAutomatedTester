class Issue:
    def __init__(
        self,
        issue_type: str,
        issue_description: str,
        issue_element: str,
        issue_link: str,
        page_title: str,
        severity: str = "low",
    ):
        self.issue_type = issue_type
        self.issue_description = issue_description
        self.issue_element = issue_element
        self.issue_link = issue_link
        self.issue_page_title = page_title
        self.severity = severity
