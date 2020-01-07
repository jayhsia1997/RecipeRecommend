from bs4 import BeautifulSoup
import multiprocessing as mp
import os,time,random,requests

x=40
y=54
human=4

user_agenttt="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
headers={"user-agent":user_agenttt,
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
"cache-control": "no-cache",
"pragma": "no-cache",
"referer": "https://food.ltn.com.tw/article/9373",
"sec-fetch-mode": "nested-navigate",
"sec-fetch-site": "cross-site",
"upgrade-insecure-requests": "1"}

path=r'./food'
if not os.path.exists(path):
    os.mkdir(path)

def producer(queue):
    list_of_title=[]
    url_first = "https://food.ltn.com.tw/category"
    res_first = requests.get(url_first, headers=headers)
    soup_first = BeautifulSoup(res_first.text, 'html.parser')
    titles_firsts = soup_first.select('p')
    for title_first in titles_firsts:
        try:
            if (title_first.a["href"] != "type/84") and (title_first.a["href"] != "type/87") and (title_first.a["href"] != "type/243")  :
                list_of_title.append(title_first.a["href"])
        except TypeError as e:
            print(e)
    for n,i in enumerate(list_of_title):
        if n+1>=x and n+1<=y :
            queue.put(i)


def worker(worker_id,queue):
    while True:
        list_of_class=[]
        title_first=queue.get()
        print(title_first)
        url_second_level = "https://food.ltn.com.tw/" + title_first + "/" + str(1)
        res_second = requests.get(url_second_level, headers=headers)
        soup_second = BeautifulSoup(res_second.text, 'html.parser')
        page_tail = soup_second.select('a[class="p_last"]')
        page_last_number = page_tail[0]['href'].split("/")[5]
        page_number = 1
        while page_number <= int(page_last_number):
            url_second_level_every_page = "https://food.ltn.com.tw/" + title_first + "/" + str(
                page_number)
            res_second_every_page = requests.get(url_second_level_every_page, headers=headers)
            soup_second_every_page = BeautifulSoup(res_second_every_page.text, 'html.parser')
            url_thrds = soup_second_every_page.select('div[data-desc="清單"] a')
            for url_thrd in url_thrds:
                no_article_thrd=url_thrd["href"].split("/")[1]
                print(no_article_thrd)
                time.sleep(random.random())
                list_of_class.append(no_article_thrd)
            print(str(page_number) + "page" + "~~~~~~~~~~~~~~~~~~~")
            page_number += 1
        title_first=str(title_first).replace("/","_")
        with open("%s/food_%s.txt"%(path,title_first), 'a+', encoding='utf-8') as f:
            str_of_class=",".join(list_of_class)
            f.write(str_of_class)
        time.sleep(30)
        queue.task_done()



def main(human):
    t0 = time.time()
    print("start")
    queue=mp.JoinableQueue()
    for i in range(human):
        worker_i=mp.Process(target=worker,args=(i,queue))
        worker_i.daemon=True
        worker_i.start()
        print(worker_i)
    producer(queue)
    queue.join()
    print(time.time()-t0, "seconds time")

if __name__ == "__main__":
    main(human)


