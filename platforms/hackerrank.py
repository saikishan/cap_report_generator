import requests,math
from platforms.generic_engine import GenericEngine
from platforms.generic_driver import GenericDriver

class HackerRankEngine(GenericEngine):
    def __init__(self, question_url, key_users):
        super().__init__(question_url,key_users)

    def generate_request_url(self, pg_id=0):
        rest_url = self.base_url.replace("hackerrank.com/", "hackerrank.com/rest/contests/master/")
        current_rest_url = rest_url + "/filter?offset={current_count}&limit=100".format(current_count=pg_id*100)
        return current_rest_url

    def get_page_data(self, url):
        print("calling for page"+ url)
        while True:
            try:
                response = requests.get(url)
            except Exception:
                print(Exception)
                continue
            break
        data = response.json()
        return data

    def get_pages_count(self, page_data):
        return math.ceil(page_data['total']//100)

    def get_users_from_page(self, page_data):
        result_li = []
        for x in page_data['models']:
            if x['score'] != 0 and x['hacker'] in self.key_users:
                result_li.add(x['hacker'])
        return result_li

    def update_matching_list(self, users_li):
        self.result_users.update(users_li)

    def scrap_the_question(self, ):
        initial_url = self.generate_request_url()
        page_data = self.get_page_data(initial_url)
        pages_count = self.get_pages_count(page_data)
        kk = 1
        while(kk < pages_count):
            page_users = self.get_users_from_page(page_data)
            self.update_matching_list(page_users)
            url = self.generate_request_url(kk)
            page_data = self.get_page_data(url)
            kk+=1
        return self.get_results()

class HackerRankDriver(GenericDriver):
    def __init__(self, question_url, given_users):
        leaderboard_url = question_url.replace('/problem', '/leaderboard')
        super().__init__(leaderboard_url , given_users, HackerRankEngine(leaderboard_url,given_users))

    def get_results(self,):
        return self.engine.scrap_the_question()


def tester():
    question ='https://www.hackerrank.com/challenges/a-very-big-sum/problem'
    users = ["17pa1a0538", "VinayV9"]
    hd = HackerRankDriver(question, users)
    print (hd.get_results())

tester()
