# -*- coding: utf-8 -*-

# for macOS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#--------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
# from selenium.webdriver import Chrome

import requests
import json
import os
# import time

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

path = r'./res'
if not os.path.exists(path):
    os.mkdir(path)

'''
#cookpad
driver = Chrome('./chromedriver')
driver.get(login_url['cookpad'])

driver.find_element_by_id('identity_authentication_identity').send_keys('jayhsia1997@gmail.com')
time.sleep(5)
driver.find_element_by_id('identity_authentication_password').send_keys('7sZSnxCAbatLN8@')
driver.find_element_by_id('login_submit').click()

#icook
driver = Chrome('./chromedriver')
driver.get(login_url['icook'])

driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form[1]/div[3]/div/div/input').send_keys('jayhsia1997@gmail.com')
time.sleep(5)
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form[1]/div[3]/div/input').send_keys('aaaaa')
'''

#globals
recipes_data = {}
recipes_data['recipes'] = []
single_recipe_data = {}

for page_num in range(1):
    print('index =', page_num)
    page_url = web_url['icook_rice'] + "?page=%s" % (page_num)
    print(page_url)
    res = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('div[class="browse-recipe-cover"]')
    # print(title)

    for recipe_list_index, recipe_list in enumerate(title):
        try:
            temp = ''
            recipe_name = recipe_list.a['title']
            recipe_url = web_url['icook'] + recipe_list.a['href']
            recipe_img = recipe_list.a.img['data-src']
            print(recipe_name + ':' + recipe_url)

            res = requests.get(recipe_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')

            post_time = soup.select('span[class="meta-content"]')[0].text.split(' ')[0].replace('/', '-')

            if temp != recipe_name:
                single_recipe_data = {}

            temp = recipe_name

            single_recipe_data = {
                'recipe_name': recipe_name,
                'recipe_url': recipe_url,
                'recipe_img_url': recipe_img,
                'post_time': post_time,
                'quantity': '1份',
                'ingredients': [],
                'cooking_steps': []
            }

            for recipe_info_index, recipe_info in enumerate(soup.select('div[class="ingredient"]')):
                try:
                    ingredient_name = recipe_info.div.a.text
                    ingredient_unit = soup.select('div[class="ingredient-unit"]')[recipe_info_index].text
                    single_recipe_data['ingredients'].append({
                        'ingredient_name': ingredient_name,
                        'ingredient_unit': ingredient_unit
                    })
                except:
                    pass
            for steps_index, steps in enumerate(soup.select('div[class="step-instruction-content"]')):
                try:
                    cooking_methods = steps.text
                    single_recipe_data["cooking_steps"].append({
                        "steps": steps_index + 1,
                        "methods": cooking_methods
                    })
                except:
                    pass

            recipes_data['recipes'].append(single_recipe_data)

            try:
                with open('%s/%s.json' % (path, recipe_name.replace('/','|')), 'w', encoding='utf-8') as outfile:
                    outfile.write(json.dumps(single_recipe_data, ensure_ascii=False))
                with open('%s/recipes_data.json' % (path), 'w', encoding='utf-8') as outfile:
                    outfile.write(json.dumps(recipes_data, ensure_ascii=False))
                print('-----')
            except OSError as e:
                # with open('%s/recipe%s.txt' % (path, i), 'w', encoding='utf-8') as f:
                #     f.write(recipe_text + '\n')
                print(e)
        except:
            pass
