from .platforms import HackerRankDriver

class Scrapie:
    def get_driver(self,question, students, colleges = None, last_scraped = None):
        if question.startswith("https://www.hackerrank.com/"):
            return HackerRankDriver(question, students, colleges)
        raise Exception("Platform Not Supported")

    def __init__(self, question, students, colleges = None, last_scraped = None):
        self.driver = self.get_driver(question, students, colleges, last_scraped)

    def get_passed_students(self):
        return self.driver.get_results()

