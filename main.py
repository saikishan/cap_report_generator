from hackerrank import Hackerrank
from codechef import Codechef
from config  import question_file_data,question_dir,result_dir
import arrow
hackerrank_scraper = Hackerrank()
def hackerrank_testing():
    hackerrank_student_l = ['15PA1A05E0']
    h_url = "https://www.hackerrank.com/challenges/a-very-big-sum/leaderboard"
    stu_dict = hackerrank_scraper.get_filtered_list_from_webpage(h_url, hackerrank_student_l)
    return stu_dict

def codechef_testing():
    cc_scraper = Codechef()
    c_url = "https://www.codechef.com/status/CHSERVE"
    codechef_student_l = ['15PA1A05E0']
    stu_dict = cc_scraper.get_filtered_list_from_webpage(c_url , codechef_student_l)
    return stu_dict

def generate_students_dict():
    with open("./students.csv",'r') as students_file:
        students_file.readline()
        students_dict = {}
        def get_one_student_dict(line):
            student = dict()
            words = [x.replace('"', '').strip() for x in line.split(",")]
            student["email"] = words[1]
            student["college_id"] = words[2]
            student["name"] = words[3]
            student["branch"] = words[4]
            student["hackerrank_profile"] = words[5]
            return student

        while(1):
            student_entry = students_file.readline()
            if not student_entry:
                break
            student = get_one_student_dict(student_entry)
            students_dict[student["college_id"]] = student

    return students_dict

def generate_questions(assignment_file_name):
    with open(assignment_file_name,'r') as assignment_file:
        assignment_file.readline()

        def get_one_question_dict(line):
            question = dict()
            words = [x.replace('"', '').strip() for x in line.split(",")]
            question["platform"] = words[0]
            question["name"] = words[1]
            question["link"] = words[2]
            return question

        while(1):
            question = assignment_file.readline()
            if not question:
                return
            yield get_one_question_dict(question)


def get_status_message(status):
    if status == True:
        return "pass"
    return "fail"

if __name__ == '__main__':
    students_dict = generate_students_dict()
    report_header = "id,name,branch,question_name,status,link,timestamp\n"
    report_template = "{id},{name},{branch},{question_name},{status},{link},{timestamp}\n"
    hacker_rank_dict = { x["hackerrank_profile"]:x["college_id"] for x in students_dict.values() }
    for file_name in question_file_data:
        assignment_file_name = "{}{}.csv".format(question_dir, file_name)
        report_file_name = "{}{}-re.csv".format(result_dir, file_name)
        with open(report_file_name,"w") as report_file:
            report_file.write(report_header)
            for question in generate_questions(assignment_file_name):
                if question["platform"] == 'hacker_rank':
                    result_dict = hackerrank_scraper.get_new_students_using_api(question["link"],hacker_rank_dict.keys())
                    for x in result_dict.keys():
                        id = hacker_rank_dict[x]
                        student = students_dict[id]
                        report_data = report_template.format(id= id,
                                                             name = student["name"], branch = student["branch"],
                                                             question_name = question["name"], status = get_status_message(result_dict[x]),
                                                             link = question["link"], timestamp= arrow.now())
                        report_file.write(report_data)
