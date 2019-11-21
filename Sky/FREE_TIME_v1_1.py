from bs4 import BeautifulSoup
import multiprocessing as mp
#from modul_hank import *
import os,time,random,requests

x=4
y=5
human=6

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

path=r'./food'  #資料夾
if not os.path.exists(path): #沒有這個資料夾就新創資料夾
    os.mkdir(path)

def producer(queue):
    list_of_title=[]
    # 第一層
    url_first = "https://food.ltn.com.tw/category"
    res_first = requests.get(url_first, headers=headers)
    soup_first = BeautifulSoup(res_first.text, 'html.parser')
    # tag p包含我要的五穀雜糧、肉類..而且五穀雜糧下面的細項不點選就已經全在五穀頁面裡面，到下層連結只要用五穀雜糧就可抓到全部
    titles_firsts = soup_first.select('p')
    for title_first in titles_firsts:
        try:
            print("~~~~~~~~~~~~~~~~~~the_second_level~~~~~~~~~~~~~~~~~~~~~")
            # 第二層第1頁
            # 跳過兩個分類，裡面頁面沒有內容，原本用except IndexError跳過，但會造成後面爬蟲在一個分類沒爬完，跳到下一個分類
            if (title_first.a["href"] != "type/84") and (title_first.a["href"] != "type/87") and (title_first.a["href"] != "type/243")  :
                list_of_title.append(title_first.a["href"])
        except TypeError as e:
            print(e)  # 在第一層有些 tag p 下面沒有 tag a
    for n,i in enumerate(list_of_title):
        if n+1>=x and n+1<=y :
            queue.put(i)  # 傳遞Type 如果先組成url worker還要將url 還原成type才能組成url_second_level_every_page


def worker(worker_id,queue):
    while True:
        list_of_class=[]
        title_first=queue.get()
        print(title_first)
        url_second_level = "https://food.ltn.com.tw/" + title_first + "/" + str(1)
        res_second = requests.get(url_second_level, headers=headers)
        soup_second = BeautifulSoup(res_second.text, 'html.parser')
        # 找最後一頁數字
        page_tail = soup_second.select('a[class="p_last"]')
        page_last_number = page_tail[0]['href'].split("/")[5]
        # print(page_last_number)
        # 第二層第1頁~最後一頁
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
                list_of_class.append(no_article_thrd)#放進list
            print(str(page_number) + "page" + "~~~~~~~~~~~~~~~~~~~")
            page_number += 1
        title_first=str(title_first).replace("/","_")
        with open("%s/food_%s.txt"%(path,title_first), 'a+', encoding='utf-8') as f:
            str_of_class=",".join(list_of_class)
            f.write(str_of_class)
        time.sleep(30)



def main(human):
    #lazy(5)
    t0 = time.time()
    print("start")
    queue=mp.JoinableQueue()
    for i in range(human+1):
        worker_i=mp.Process(target=worker,args=(i+1,queue))
        worker_i.daemon=True
        worker_i.start()
        print(worker_i)
    producer(queue)
    queue.join()
    print(time.time()-t0, "seconds time")
if __name__ == "__main__":
    main(5) #worker數目


