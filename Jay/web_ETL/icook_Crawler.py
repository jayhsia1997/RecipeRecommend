# -*- coding: utf-8 -*-

# for macOS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# --------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
# from selenium.webdriver import Chrome

import requests
import json
import os
import sys
import pymongo
# import time

def takeSecond(elem):
    return elem[1]

def icook_ETL(web_url, categories_index, run_pages=1):
    # globals
    recipes_data = {}
    recipes_data['recipes'] = []
    single_recipe_data = {}

    for page_num in range(run_pages):
        try:
            page_url = web_url + '/categories/' + str(categories_index) + "?page=%s" % (page_num)
            res = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.select('div[class="browse-recipe-cover"]')
            categories_name = soup.select('h2[class="category-name"]')[0].text.replace(' ', '').replace('\n', '')

            categories_name_path = r'./res/recipes/' + categories_name
            if not os.path.exists(categories_name_path):
                os.mkdir(categories_name_path)
            print(categories_name)

            # recipe information
            for recipe_list_index, recipe_list in enumerate(title):
                try:
                    temp = ''
                    recipe_name = recipe_list.a['title']
                    recipe_url = web_url + recipe_list.a['href']
                    recipe_img = recipe_list.a.img['data-src']
                    print(recipe_name + ':' + recipe_url)

                    # post time
                    res = requests.get(recipe_url, headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    post_time = soup.select('span[class="meta-content"]')[0].text.split(' ')[0].replace('/', '-')

                    if temp != recipe_name:
                        single_recipe_data = {}

                    temp = recipe_name

                    # json dumps format
                    single_recipe_data = {
                        'recipe_name': recipe_name,
                        'recipe_url': recipe_url,
                        'recipe_img_url': recipe_img,
                        'post_time': post_time,
                        'quantity': 1,
                        'ingredients': [],
                        'cooking_steps': []
                    }

                    # ingredients
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
                    # cooking_methods
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
                except:
                    print(sys.exc_info())
                # save file to mongo
                try:
                    db.recipes_db.insert_one(single_recipe_data)
                except:
                    print(sys.exc_info())
        except:
            print(sys.exc_info())

def categories():
    temp_list = []
    res = requests.get(web_url['icook_categories'], headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    temp = soup.select('li[class="categories-all-child"]')

    for i, temp_c in enumerate(temp):
        categories_name = temp_c.a['name']
        categories_index = int(temp_c.a['href'].split('/')[2])
        temp_list.append((categories_name, categories_index))

    temp_list.sort(key=takeSecond)

    recipes_categories = {'_id':1}
    recipes_categories['categories'] = []

    for j, categories in enumerate(temp_list):
        recipes_categories['categories'].append({categories[0]: categories[1]})

    try:
        if db.recipes_categories.find_one({'_id':1}) != None:
            print("id exist")
        elif db.recipes_categories.find_one() == None:
            db.recipes_categories.insert_one(recipes_categories)
            print('insert done')
        else:
            print("id exist")
    except:
        print(sys.exc_info())

def load_file():
    try:
        read_categories = db.recipes_categories.find_one()
        print(read_categories)
        for i, temp in enumerate(read_categories['categories']):
            recipes_categories.update(temp)
    except:
        print(sys.exc_info())
    return recipes_categories

def main():
    print('-----')

    categories()
    load_file()

    print(recipes_categories['米食'])

    icook_ETL(web_url['icook'], recipes_categories['米食'])

if __name__ == '__main__':
    path = r'./res'
    path2 = r'./res/recipes'
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path2):
        os.mkdir(path2)

    # user agent
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    headers = {'User-Agent': user_agent}
    web_url = {'cookpad': 'https://cookpad.com/tw',
               'icook': 'https://icook.tw',
               'icook_popular': 'https://icook.tw/recipes/popular',
               'icook_categories': 'https://icook.tw/categories',
               'icook_rice': 'https://icook.tw/categories/46'
               }

    # mongo connect set
    client = pymongo.MongoClient('mongodb://%s:%s@10.120.38.13' % ("root", "root"), 27017)
    db = client.test

    recipes_categories = {}

    main()