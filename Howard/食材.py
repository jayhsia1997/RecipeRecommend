#!/usr/bin/env python
# coding: utf-8

# In[8]:


#先跑這個做文章擷取
def gg(url):
    global na #全域變數
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    本體 = soup.select('div[id="main-content"]') #文章body
    
    

    author = 'NA' #作者
    title = 'NA' #標題
    time = 'NA' #時間
    try: #設定文字檔編輯順序
        author = 本體[0].select('span[class="article-meta-value"]')[0].text
        title = 本體[0].select('span[class="article-meta-value"]')[2].text
        time = 本體[0].select('span[class="article-meta-value"]')[3].text
        dele = f'作者{author}看板cookclub標題{title}時間{time}' #dele自行設定的變數用來刪除作者標題時間只留內文 #f做正規化
        本體 = 本體[0].text.replace(dele,'')
        s = ['\\',':','*','"','/','?','|','<','>'] #文字檔名稱不能出現的符號
        for i in s:
            if i in title:
                title = title.replace(i,' ')
    except:
        本體 = 本體[0].text
    #若標題為'NA'的編輯方式
    if title == 'NA':
        
        with open (f'E:\\food\\NA{na}.txt','w',encoding='utf-8') as w:
            w.write(f'標題: {title}\n')
            w.write(f'作者: {author}\n')
            w.write(f'發文時間 {time}\n')
            w.write(本體)
        na +=1    
    else:    
        with open (f'E:\\food\\{title}.txt','w',encoding='utf-8') as w:#文字檔存的位置
            w.write(f'標題: {title}\n')
            w.write(f'作者: {author}\n')
            w.write(f'發文時間 {time}\n')
            w.write(本體)


# In[9]:


import requests
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
page_number = 3826
na = 0 #標題為NA的比數從0開始
while page_number >= 3820:
    print(page_number)
    url = 'https://www.ptt.cc/bbs/cookclub/index.html'
    url = 'https://www.ptt.cc/bbs/cookclub/index3826.html'
    url = 'https://www.ptt.cc/bbs/cookclub/index%s.html'%(page_number)
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article_title_html = soup.select('div[class="title"]')
    for each_article in article_title_html:
        try:            
            print(each_article.a.text)
            print('https://www.ptt.cc/'+each_article.a['href'])
            url = 'https://www.ptt.cc/'+each_article.a['href']
            gg(url)
            print()
        except:
            print('============')
    page_number -= 1


# In[18]:


import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
source_path = r'E:\food' #讀取資料夾位子
file_list = os.listdir(source_path) #列出資料夾所有檔案名稱
df_list = []
for article in file_list: #article每一個檔案的文章內容會是一個字串
    with open(source_path + '/' + article, 'r', encoding='UTF-8') as f:
        tem_str = f.read() #讀出所有文章內容
    #   print(tem_str)
        info_list = tem_str.split('--\n※ 發信站: 批踢踢實業坊(ptt.cc)')[0]
    #用split分割文章(以\n空格分隔)取第一部分[0]

    try:
        info_list = tem_str.split('--\n※ 發信站: 批踢踢實業坊(ptt.cc)')[0]
    except IndexError as e:
        print(e.args)#把錯誤訊息print出來
print(info_list)


# In[19]:


df = pd.DataFrame(columns=['標題','作者','發文時間','食譜'])


# In[20]:


index = 0


# In[21]:


def gg(url):
    global index
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    本體 = soup.select('div[id="main-content"]') #文章body
    
    

    author = 'NA' #作者
    title = 'NA' #標題
    time = 'NA' #時間
    try: #設定文字檔編輯順序
        author = 本體[0].select('span[class="article-meta-value"]')[0].text
        title = 本體[0].select('span[class="article-meta-value"]')[2].text
        time = 本體[0].select('span[class="article-meta-value"]')[3].text
        dele = f'作者{author}看板cookclub標題{title}時間{time}' #dele自行設定的變數用來刪除作者標題時間只留內文 #f做正規化
        本體 = 本體[0].text.replace(dele,'')

    except:
        本體 = 本體[0].text
        
    df.loc[index] = [title,author,time,本體]
    index+=1
    


# In[22]:


page_number = 3826
na = 0 #標題為NA的筆數從0開始
while page_number >= 3820:
    print(page_number)
    url = 'https://www.ptt.cc/bbs/cookclub/index.html'
    url = 'https://www.ptt.cc/bbs/cookclub/index3826.html'
    url = 'https://www.ptt.cc/bbs/cookclub/index%s.html'%(page_number)
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    article_title_html = soup.select('div[class="title"]')
    for each_article in article_title_html:
        try:            
            print(each_article.a.text)
            print('https://www.ptt.cc/'+each_article.a['href'])
            url = 'https://www.ptt.cc/'+each_article.a['href']
            gg(url)
            print()
        except:
            print('============')
    page_number -= 1


# In[23]:


df


# In[24]:


df.to_json("這裡放檔案路徑+檔名.json",orient='index',force_ascii=False) #存成JSON


# In[25]:


df.to_excel("這裡放檔案路徑+檔名.xlsx",encoding='utf-16') #存成EXCEL


# In[ ]:




