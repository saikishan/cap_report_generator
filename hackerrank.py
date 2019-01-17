from bs4 import BeautifulSoup
import urllib.request
import threading
import requests
class Hackerrank:
    def get_count_of_pages(self, url):
        print("page-count url" + url)
        content = urllib.request.urlopen(url).read()
        soup  = BeautifulSoup(content,features="html.parser")
        page_count = int(soup.body.find(class_="page-item last-page", recursive=True).a.get("data-attr8"))
        return page_count

    def get_username(self, row):
        try:
            name = row.find(recursive=True, attrs = {"data-analytics" : "LeaderboardListUserName"}).text
            rank = int(row.find(recursive=True, class_ = "table-row-column ellipsis rank" ).div.text)
        except AttributeError as ae:
            print(ae)
            return None
        if rank == 1:
            return name
        return None

    def scan_the_page(self, url, student_dict, page_id):
        print("in page no " + str(page_id))
        current_url = url + "?limit=100&page={}".format(page_id)
        content = None
        while content is None:
            try:
                content = urllib.request.urlopen(current_url).read()
            except Exception as e:
                print(e)
        soup = BeautifulSoup(content, features="html.parser")
        user_table = soup.findAll(class_="table-row-wrapper", recursive=True)
        for row in user_table:
            name = self.get_username(row)
            print(name)
            if name and name in student_dict:
                student_dict[name] = True

    def thread_caller(self, url, page_start, page_end, student_dict):
        print("strart page ", page_start, "end page" , page_end )
        for x in range(page_start, page_end):
            self.scan_the_page(url, student_dict, x)

    def get_filtered_list_from_webpage(self, url, student_list):
        initial_page_url = url + "?limit=100&page=1"
        pagecount = self.get_count_of_pages(initial_page_url)
        student_dict = { x:False for x in student_list}
        print("page_count", pagecount)
        def divide_to_sets(pagecount,no_of_threads):
            share = pagecount // no_of_threads
            if share < 1:
                yield(1,pagecount)
                return
            yield (1, 1*share)
            for x in range(1,no_of_threads-1):
                yield (x*share,(x+1)*share)
            yield((no_of_threads-1)*share,pagecount+1)

        thread_list = []
        for x in divide_to_sets(pagecount, 8):
            thread = threading.Thread(target=self.thread_caller,args=(url,x[0],x[1],student_dict))
            thread.start()
            thread_list.append(thread)

        for x in thread_list:
            x.join()
        return student_dict

    def get_new_students_using_api(self, url, student_list):
        current_count = 0
        rest_url = url.replace("hackerrank.com/","hackerrank.com/rest/contests/master/")
        current_rest_url = rest_url + "/filter?offset={current_count}page&limit=100&include_practice=true&school=Vishnu%20Institute%20Of%20Technology&filter_kinds=school".format(current_count = current_count)
        response = requests.get(current_rest_url)
        data = response.json()
        total_count = data['total']
        student_dict = {x: False for x in student_list}
        while(total_count):
            for x in data['models']:
                total_count-=1
                print(x['hacker'])
                if x['rank']==1 and x['hacker'] in student_dict:
                    student_dict[ x['hacker'] ] = True
            if total_count:
                current_count+=1
                current_rest_url = rest_url + "/filter?offset={current_count}page&limit=100&include_practice=true&school=Vishnu%20Institute%20Of%20Technology&filter_kinds=school".format(
                    current_count=current_count)
                response = requests.get(current_rest_url)
                data = response.json()
        return student_dict
    
        
