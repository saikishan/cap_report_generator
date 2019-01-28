from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import threading
#implementation to be modified
class Codechef:
    def get_count_of_pages(self, url):
        print("page-count url" + url)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        content = urlopen(req).read()
        soup  = BeautifulSoup(content,features="html.parser")
        line = soup.body.find(class_="pageinfo", recursive=True).text
        number = line[line.find('f')+1:]
        page_count = int(number)
        return page_count

    def get_username(self, row):
        try:
            name = row.a.get("title")
        except AttributeError as ae:
            print(ae)
            return None
        return name

    def scan_the_page(self, url, student_dict, page_id):
        print("in page no " + str(page_id))
        current_url = url + "?page={}&sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO".format(page_id)
        content = None
        while content is None:
            try:
                req = Request(current_url, headers={'User-Agent': 'Mozilla/5.0'})
                content = urlopen(req).read()
            except Exception as e:
                print(e)
        soup = BeautifulSoup(content, features="html.parser")
        rows  = soup.body.findAll(recursive=True, attrs = {"width" : "144"})    
        for row in rows:
            name = self.get_username(row)
            print(name)
            if name and name in student_dict:
                student_dict[name] = True

    def thread_caller(self, url, page_start, page_end, student_dict):
        print("strat page ", page_start, "end page" , page_end )
        for x in range(page_start, page_end):
            self.scan_the_page(url, student_dict, x)

    def get_filtered_list_from_webpage(self, url, student_list):
        initial_page_url = url + "?page={}&sort_by=All&sorting_order=asc&language=All&status=15&handle=&Submit=GO".format(0)
        pagecount = self.get_count_of_pages(initial_page_url)
        student_dict = { x:False for x in student_list}
        print("page_count", pagecount)

        def divide_to_sets(pagecount,no_of_threads):
            share = pagecount // no_of_threads
            if share < 1:
                yield(1,pagecount)
                return
            yield (0, 1*share)
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