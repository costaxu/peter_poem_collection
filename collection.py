# coding: utf-8
import requests
import time
import bs4

class Work:
    def __init__(self):
        return

def fetch_works(member_id, max_page):
    url_template = "https://www.52shici.com/collection.php?mem_id=%d&page=%d"
    works = []
    for page in range(1, max_page+1):
        url = url_template % (member_id, page)
        response = requests.get(url)
        print(url)
        time.sleep(1)
        if response.status_code != 200:
            print("get page %d failed, http status code" % (page, response.status_code))
            return

        soup = bs4.BeautifulSoup(response.content, 'html.parser')
        lists = soup.find_all('ul', {"class": "my-works-list"})[0].find_all('li')
        for li in lists:
            # print(li)
            work = Work()

            work.url = li.a.attrs['href']
            work.title = li.a.text
            work.top = False
            if "【置顶】" in work.title:
                work.top = True
                work.title = work.title.strip("【置顶】")

            if work.top:
                work.classification = li.find_all('span')[1].text
                work.date = li.find_all('span')[2].text
            else:
                work.classification = li.find_all('span')[0].text
                work.date = li.find_all('span')[1].text

            work.url = "https://www.52shici.com/" + work.url
            # print(work.url, "title=" + work.title, "classfication=" + work.classification, "date=" + work.date)
            if work.top == True:
                if page == 1:
                    # 如果是置顶，只有第一页才加入
                    works.append(work)
            else:
                works.append(work)
        print("work count:", len(works))

    result_f = open("result.txt", "w")
    print("work count:", len(works))
    for work in works:
        work_response = requests.get(work.url)
        time.sleep(1)
        if work_response.status_code != 200:
            print("get work %s, url %s, failed, http status code" % (work.title, work.url, work_response.status_code))
            continue
        print("get url:", work.url)
        work_soup = bs4.BeautifulSoup(work_response.content, 'html.parser')
        work.intro = work_soup.find('p', {"class": "works-intro"}).text
        work.content = work_soup.find('div', {"class": "works-content"}).text
        result_f.write(work.title + "\r\n")
        result_f.write(work.classification + "\r\n")
        result_f.write(work.date + "\r\n")
        result_f.write(work.intro + "\r\n")
        result_f.write(work.content + "\r\n\r\n")
    result_f.close()


