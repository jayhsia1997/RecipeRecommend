import requests,os
from bs4 import BeautifulSoup

useragent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
headers = {'User-agent': useragent}
path = r'./res'
if not os.path.exists(path):
    os.mkdir(path)

url = "https://www.dimcook.com/tag/%E4%B8%AD%E5%BC%8F"
res = requests.get(url, headers = headers)
#print(res)
soup = BeautifulSoup(res.text, 'html.parser')

#print(soup)
title = soup.select('li[class="result-item result-item-white"]')
#print(title)

for temp_title in title:
        try:
            print(temp_title.img.text)
            article_url = 'https://dimcook.com' + temp_title.a['href']
            res_article = requests.get(article_url, headers=headers)
            soup_article = BeautifulSoup(res_article.text, 'html.parser')
            #article_str = article_content[0].text.split('--')[0]
            #print(article_content)
            article_content = soup_article.select('div[id="recipePhotos"]')
            article_content2 = soup_article.select('li[rel="v:ingredient"]')

            for tag_inset in article_content:
                print("食譜名稱:"+tag_inset.img["title"])
                print('食譜網址:https://dimcook.com' + temp_title.a['href'])
                print("食譜圖片連結:"+tag_inset.a["href"])
                print("食材:")

            for tag_inset2 in article_content2:
                #print(tag_inset2)
                print(tag_inset2.span.text)
                #print(tag_inset2.select('span[class="ingredientAmt"]'))
                out = tag_inset2.select('span[class="ingredientAmt"]')
                for out1 in out:
                    print(out1["content"])


        except ArithmeticError as e:
            print('===================')
            print(temp_title)
            print(e.args)
            print('===================')

