import multiprocessing as mp
from multiprocessing import Queue
import os
import random
import time, re
import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup


def pre_manager(key, page, page_jq):
    task = [0, '']
    task[0] = key
    task[1] = page
    page_jq.put(task)


def pre_crawler(pre_crawler_id, page_jq, url_jq):

    while True:
        task = list(page_jq.get())
        page = task[1]
        user_url = f'https://www.pixnet.net/blog/articles/category/27/hot/{page}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

        res = requests.get(user_url, headers=headers)
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        for k in range(1, 11):
            try:
                href = soup.select('div[class="box-body"]')[0].select(f'li[class="rank-{k}"]')[0].a['href']

                url_jq.put(href)
                print(f'pre_crawler {pre_crawler_id} finished tag {task[1]}')
            except:
                pass



        page_jq.task_done()


def final_crawler(final_crawler_id, url_jq, data_q):
    while True:
        link = url_jq.get()
        driver = webdriver.Chrome('./chromedriver.exe')
        driver.get(link)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

        res = requests.get(link, headers=headers)
        if res.ok == True:
            author = ''
            title = ''
            post_date = ''
            hit = ''
            tag = ''
            word = ''

            res.encoding = 'UTF-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            try:
                author = soup.select('meta[name="author"]')[0].attrs['content']
            except:
                pass

                try:
                    title = soup.select('title')[0].text
                except:
                    print(link)
                    pass

            try:
                post_date = soup.select('li[class="publish"]')[0].text
            except:
                pass

            try:
                text = soup.select('div[id="article-content-inner"]')
                for i in text:
                    word += i.text
            except:
                pass

            try:
                tags = soup.select('div[class="tag__main"]')[0].select('a')

                for t in tags:
                    tag += t.text.strip()
                    tag += ' '
            except:
                pass

            driver.get(link)
            try:
                hit = driver.find_elements_by_class_name("author-views")[0].text
            except:
                pass
            driver.close()
            data_q.put([title, author, post_date, hit, tag, link, word])




        print(f'final_crawler {final_crawler_id} finished url {link}')
        url_jq.task_done()


def main():
    page_list = [i for i in range(1)]#放頁數

    page_jq = mp.JoinableQueue()
    url_jq = mp.JoinableQueue()


    for key, page in enumerate(page_list):
        pre_manager(key, page, page_jq)

    for i in range(1,3):
        name = f'pre_crawler_{i}'
        name = mp.Process(target=pre_crawler, args=(i, page_jq, url_jq))
        name.daemon = True
        name.start()

    for j in range(1,3):
        name = f'final_crawler_{j}'
        name = mp.Process(target=final_crawler, args=(j, url_jq, data_q))
        name.daemon = True
        name.start()


    page_jq.join()
    url_jq.join()

    print(url_jq.qsize())
if __name__ == "__main__":
    data_q = Queue()
    main()
    df = pd.DataFrame(columns=['_id', '作者', '打卡地點', '讚數', '發文時間', '標籤', '文章內容'])

    for i in range(data_q.qsize()):
        tmp = data_q.get()
        if tmp[0] not in list(df['_id']):
            df.loc[i] = tmp
    # pip install openpyxl如果無法存取Excel輸入後強制除錯
    df.to_excel("E:\\pixnet\\pixnet.xlsx", encoding='utf-16')
    df.to_json('E:\\pixnet\\pixnet.json',
               orient='index',force_ascii=False)
    working_time = time.perf_counter()
    print(f'Used {round(working_time / 3600, 2)} hrs')
