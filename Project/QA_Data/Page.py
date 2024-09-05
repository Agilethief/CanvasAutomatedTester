class Page:

    def __init__(self, url, course):
        self.url = url
        self.title = "page"
        self.link_count = 0
        self.links = []
        self.word_count = 0
        self.image_count = 0
        self.course = course
