from hackerrank import Hackerrank
from codechef import Codechef
#this is to get all table records >>> body.findAll(class_="table-row-wrapper", recursive=True)
def hackerrank_testing():
    hr_scraper = Hackerrank()
    hackerrank_student_l = ['15PA1A05E0']
    h_url = "https://www.hackerrank.com/challenges/a-very-big-sum/leaderboard"
    stu_dict = hr_scraper.get_filtered_list_from_webpage(h_url, hackerrank_student_l)
    return stu_dict

def codechef_testing():
    cc_scraper = Codechef()
    c_url = "https://www.codechef.com/status/CHSERVE"
    codechef_student_l = ['15PA1A05E0']
    stu_dict = cc_scraper.get_filtered_list_from_webpage(c_url , codechef_student_l)
    return stu_dict

print(codechef_testing())