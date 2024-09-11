from abc import ABC, abstractmethod


class I_Statable(ABC):
    @abstractmethod
    def get_id(self):
        pass

    @property
    @abstractmethod
    def get_title(self):
        pass

    @property
    @abstractmethod
    def get_url(self):
        pass

    @property
    @abstractmethod
    def get_published(self):
        pass

    @property
    @abstractmethod
    def get_issue_count(self):
        pass

    @property
    @abstractmethod
    def get_course(self):
        pass

    @property
    @abstractmethod
    def get_word_count(self):
        pass

    @property
    @abstractmethod
    def get_link_count(self):
        pass

    @property
    @abstractmethod
    def get_image_count(self):
        pass
