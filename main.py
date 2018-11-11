from hackerrank import Hackerrank

#this is to get all table records >>> body.findAll(class_="table-row-wrapper", recursive=True)
hr_scraper = Hackerrank()
Hacker_rank_student_l = ['15PA1A05E0']
url = "https://www.hackerrank.com/challenges/a-very-big-sum/leaderboard"
stu_dict = hr_scraper.get_filtered_list_from_webpage(url, student_l)