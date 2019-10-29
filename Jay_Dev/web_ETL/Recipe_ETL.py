# -*- coding: utf-8 -*-

# from urllib import request
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import time
import requests
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'

headers = {'User-Agent': user_agent}
login_url = {'cookpad':'https://cookpad.com/tw/%E7%99%BB%E5%85%A5',
             'icook':'https://icook.tw/login?ref=nav',
             }
web_url = {'cookpad': 'https://cookpad.com/tw',
           'icook': 'https://icook.tw',
           'icook_popular': 'https://icook.tw/recipes/popular',
           'icook_rice':'https://icook.tw/categories/46'
           }

#cookpad
'''
driver = Chrome('./chromedriver')
driver.get(login_url['cookpad'])

driver.find_element_by_id('identity_authentication_identity').send_keys('jayhsia1997@gmail.com')
time.sleep(5)
driver.find_element_by_id('identity_authentication_password').send_keys('7sZSnxCAbatLN8@')
driver.find_element_by_id('login_submit').click()
'''

#icook
'''
driver = Chrome('./chromedriver')
driver.get(login_url['icook'])

driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form[1]/div[3]/div/div/input').send_keys('jayhsia1997@gmail.com')
time.sleep(5)
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form[1]/div[3]/div/input').send_keys('aaaaa')
'''

path = r'./res'
if not os.path.exists(path):
    os.mkdir(path)

# recipe_ingredients = {}
ingredients = ''
for page_num in range(1,5):
    print('index =', page_num)
    page_url = web_url['icook_rice'] + "?page=%s" % (page_num)
    print(page_url)
    res = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # title = soup.select('div[class="browse-recipe-preview"]')
    title = soup.select('div[class="browse-recipe-cover"]')
    # print(title)

    for i, recipe_list in enumerate(title):
        try:
            temp_title = ''
            recipe_title = recipe_list.a['title']
            recipe_url = web_url['icook'] + recipe_list.a['href']
            recipe_img = recipe_list.a.img['data-src']
            print(recipe_title + ':' + recipe_url)
            res = requests.get(recipe_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')

            if temp_title != recipe_title:
                # recipe_ingredients = {}
                ingredients = ''
            temp_title = recipe_title

            for j, recipe_info in enumerate(soup.select('div[class="ingredient"]')):
                try:
                    # print('食材')
                    ingredient_name = recipe_info.div.a.text
                    # print(ingredient_name)
                    ingredient_unit = soup.select('div[class="ingredient-unit"]')[j].text
                    # print(ingredient_unit)
                    # recipe_ingredients.update({ingredient_name: ingredient_unit})
                    ingredients += '\t' + ingredient_name + ': ' + ingredient_unit + '\n'
                except:
                    pass
            print(ingredients)
            # print(recipe_ingredients)
            recipe_text = '料理名稱: ' + recipe_title + '\n'
            recipe_text += '料理網址: ' + recipe_url + '\n'
            recipe_text += '料理圖片: ' + recipe_img + '\n'
            recipe_text += '食材:\n' + ingredients
            try:
                with open('%s/%s.txt' % (path, recipe_title.replace('/','|')), 'w', encoding='utf-8') as f:
                    f.write(recipe_text)
                    a = 1
            except OSError as e:
                with open('%s/recipe%s.txt' % (path, i), 'w', encoding='utf-8') as f:
                    f.write(recipe_text + '\n')

        except:
            pass




'''
page_number = 6504
while page_number >= 6503:
    print('index =', page_number)
    url = 'https://www.ptt.cc/bbs/NBA/index%s.html'%(page_number)

    res = requests.get(url, headers = headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)

    title = soup.select('div[class="r-ent"] div[class="title"]')

    for n, temp_title in enumerate(title):
        try:
            title_text = temp_title.a.text
            # print(title_text)
            article_url = web_url + temp_title.a['href']
            # print(article_url)

            article_res = requests.get(article_url, headers = headers)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')

            push_up = 0
            push_down = 0
            score = 0
            author = ''
            title = ''
            datetime = ''
            try:
                article_str = article_soup.select('div[id="main-content"]')[0].text.split('--')[0]
                push_list = article_soup.select('div[class="push"] span')
                for p in push_list:
                    if '噓' in p.text:
                        push_down += 1
                    if '推' in p.text:
                        push_up += 1
                article_info = article_soup.select('div[class="article-metaline"] span')
                for n, info in enumerate(article_info):
                    if (n + 1) % 6 == 2:
                        author = info.text
                    if (n + 1) % 6 == 4:
                        title = info.text
                    if (n + 1) % 6 == 0:
                        datetime = info.text
                score = push_up - push_down
                article_str += '\n---split---\n'
                article_str += '推: %s\n' % (push_up)
                article_str += '噓: %s\n' % (push_down)
                article_str += '分數: %s\n' % (score)
                article_str += '作者: %s\n' % (author)
                article_str += '標題: %s\n' % (title)
                article_str += '時間: %s\n' % (datetime)
                try:
                    with open('%s/%s.txt' % (path, title_text), 'w', encoding='utf-8') as f:
                        f.write(article_url + '\n')
                        f.write(article_str + '\n')
                except OSError as e:
                    with open('%s/article%s.txt' % (path, n), 'w', encoding='utf-8') as f:
                        f.write(article_url + '\n')
                        f.write(article_str + '\n')

            except FileNotFoundError as e:
                print('==========')
                print(article_url)
                print(e.args)
                print('==========')

        except AttributeError as e:
            print('-----------------')
            print(temp_title)
            print(e.args)
            print('-----------------')

    page_number -= 1
'''

