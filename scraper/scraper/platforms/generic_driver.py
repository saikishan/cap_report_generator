from abc import ABC, abstractmethod

class GenericDriver(ABC):
    def __init__(self, question_url, given_users, engine):
        self.question_url = question_url
        self.given_users = given_users
        self.engine = engine


    #get the results from the engine
    @abstractmethod
    def get_results(self,):
        pass