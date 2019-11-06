import requests
from bs4 import BeautifulSoup
import os

path = r'./cook123'
if not os.path.exists(path):
    os.mkdir(path)

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
headers = {"User-agent": user_agent}

page_number = 3059

while page_number < 3065:
    url = 'https://www.wecook123.com/?p=%s'%(page_number)

    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.select('h1[class="entry-title fusion-post-title"]')
    print("料理名稱:"+title[0].text)

    print("料理網址:"+url)

    picture_url = 'https://www.wecook123.com/?p=%s'%((page_number)+1)

    res_p = requests.get(picture_url, headers=headers)

    soup_p = BeautifulSoup(res_p.text, 'html.parser')

    print("圖片網址:"+picture_url)





    page_number += 1