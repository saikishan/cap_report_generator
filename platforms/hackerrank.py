import requests,math
from platforms.generic_engine import GenericEngine
from platforms.generic_driver import GenericDriver
from utils.my_logger import MyLogger
import logging
logging.setLoggerClass(MyLogger)
logging.basicConfig()
log = logging.getLogger(__name__)

"""
after per the study made on the hackerrank
scraping the hackerrank based on time is not reliable
so college filtration in mandatory to support hacker rank adding to support for supported colleges
"""
class HackerRankEngine(GenericEngine):
    def __init__(self, question_url, key_users, schools):
        super().__init__(question_url,key_users)
        self.schools = schools
        self.config = {
            "students_per_request":100
        }

    def generate_request_url(self, **kwargs):
        rest_url = self.base_url.replace("hackerrank.com/", "hackerrank.com/rest/contests/master/")
        current_rest_url = rest_url + "/filter?offset={off_set}&limit={limit}&&include_practice=true&filter_kinds=school&school={school}"
        students_per_request = self.config["students_per_request"]
        return current_rest_url.format(off_set=(kwargs.get('pg_id',0)*students_per_request),limit=((kwargs.get('pg_id',0)+1)*students_per_request),school=kwargs.get('school'))

    def get_page_data(self, url):
        log.debug("calling for page"+ url)
        while True:
            try:
                response = requests.get(url)
            except Exception as e:
                log.error("exception in page_request", Excepion = e)
                continue
            break
        data = response.json()
        return data

    def get_pages_count(self, page_data):
        students_per_request = self.config["students_per_request"]
        return math.ceil(page_data['total'] / students_per_request)

    def get_users_from_page(self, page_data):
        result_li = []
        for x in page_data['models']:
            if x['score'] != 0 and x['hacker'] in self.key_users:
                result_li.append(x['hacker'])
        return result_li

    def update_matching_list(self, users_li):
        self.result_users.update(users_li)

    def scrap_the_question_for_school(self, school):
        initial_url = self.generate_request_url(school=school)
        page_data = self.get_page_data(initial_url)
        pages_count = self.get_pages_count(page_data)
        pg = 1
        while True:
            page_users = self.get_users_from_page(page_data)
            self.update_matching_list(page_users)
            if (pg == pages_count):
                break
            url = self.generate_request_url(pg_id=pg, school=school)
            page_data = self.get_page_data(url)
            pg += 1

    def scrap_the_question(self,):
        for school in self.schools:
            self.scrap_the_question_for_school(school)
        return self.get_results()

class HackerRankDriver(GenericDriver):
    def __init__(self, question_url, given_users, schools):
        leaderboard_url = question_url.replace('/problem', '/leaderboard')
        super().__init__(leaderboard_url , given_users, HackerRankEngine(leaderboard_url, given_users, schools))

    def get_results(self,):
        return self.engine.scrap_the_question()


def tester():
    question ='https://www.hackerrank.com/challenges/a-very-big-sum/problem'
    users = ["13PA1A05A4", "VinayV9"]
    hd = HackerRankDriver(question, users, ['Vishnu%20Institute%20Of%20Technology'])
    print (hd.get_results())

tester()
