from abc import ABC, abstractmethod

class GenericEngine(ABC):

    def __init__(self, question_url, key_users):
        self.base_url = question_url
        self.key_users = key_users
        self.result_users = set()
        self.current_webpage = None

    #current webpage is the current page and this should not be passes as message
    @abstractmethod
    def get_page_data(self, url):
        #this will get the webpage and return here we use request headers and content
        pass

    @abstractmethod
    def generate_request_url(self, **kwargs):
        #to generate the leaderbord url from the
        pass

    @abstractmethod
    def get_pages_count(self, page):
        #this whould return not of pages it should scrap to return the result
        pass

    @abstractmethod
    def get_users_from_page(self, page):
        #this will return a set of userids in that page
        pass

    @abstractmethod
    def update_matching_list(self, ):
        #this would be returning the matched set of users and add them to the users_result_set from the currentpage
        pass

    @abstractmethod
    def scrap_the_question(self, ):
        pass

    def get_results(self):
        return self.result_users