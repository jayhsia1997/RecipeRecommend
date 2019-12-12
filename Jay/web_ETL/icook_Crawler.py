# -*- coding: utf-8 -*-

import threading
import time
import pymongo
import sys
import os
import json
import requests
import re
from bs4 import BeautifulSoup
# for macOS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# --------------------------------------------------------------------------------------------------


def worker(worker_id, web_url, categories_index, collection_name, mongo_id=0):
    print("Worker: ", worker_id)
    icook_ETL(web_url=web_url, categories_index=categories_index,
              collection_name=collection_name, mongo_id=mongo_id)


def takeSecond(elem):
    return elem[1]


def icook_ETL(web_url, categories_index, collection_name, mongo_id):
    # globals
    recipes_data = {}
    recipes_data['recipes'] = []
    single_recipe_data = {}
    
    # Database collection
    db_collection = db[collection_name]
    # print(db_collection)
    
    # Get the total number of pages in the recipe category
    total_count_url = web_url + '/categories/' + str(categories_index)
    total_count_res = requests.get(total_count_url, headers=headers)
    total_count_soup = BeautifulSoup(total_count_res.text, 'html.parser')
    total_count_head = total_count_soup.select('head')
    total_count = re.sub(r'[^0-9]', '',total_count_head[0].title.text)
    run_pages = int(total_count)//18
    
    for page_num in range(1):
        try:
            page_url = web_url + '/categories/' + \
                str(categories_index) + "?page=%s" % (page_num)
            res = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = soup.select('div[class="browse-recipe-cover"]')

            # recipe information
            for recipe_list_index, recipe_list in enumerate(title):
                try:
                    temp = ''
                    quantity = 1
                    recipe_name = recipe_list.a['title']
                    recipe_url = web_url + recipe_list.a['href']
                    recipe_img = recipe_list.a.img['data-src']
                    print(recipe_name + ':' + recipe_url)

                    # post time
                    res = requests.get(recipe_url, headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    post_time = soup.select(
                        'span[class="meta-content"]')[0].text.split(' ')[0].replace('/', '-')
                    
                    # quantity
                    quantity_temp = soup.select('div[class="servings-info info-block"]')
                    
                    if quantity_temp != []:
                        quantity = int(quantity_temp[0].span.text)

                    if temp != recipe_name:
                        single_recipe_data = {}
                        mongo_id += 1

                    temp = recipe_name

                    # json dumps format
                    single_recipe_data = {
                        '_id': mongo_id,
                        'recipe_name': recipe_name,
                        'recipe_url': recipe_url,
                        'recipe_img_url': recipe_img,
                        'post_time': post_time,
                        'quantity': quantity,
                        'ingredients': [],
                        'cooking_steps': []
                    }

                    # ingredients
                    for recipe_info_index, recipe_info in enumerate(soup.select('div[class="ingredient"]')):
                        try:
                            ingredient_name = recipe_info.div.a.text
                            ingredient_unit = soup.select(
                                'div[class="ingredient-unit"]')[recipe_info_index].text
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
                    # db_collection.insert_one(single_recipe_data)
                    print(mongo_id)
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

    recipes_categories = {'_id': 1}
    recipes_categories['categories'] = []

    for j, categories in enumerate(temp_list):
        recipes_categories['categories'].append({categories[0]: categories[1]})

    try:
        if db.recipes_categories.find_one({'_id': 1}) != None:
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
        # print(read_categories)
        for i, temp in enumerate(read_categories['categories']):
            recipes_categories.update(temp)
    except:
        print(sys.exc_info())
    return recipes_categories


def main():
    print('-----')

    # save categories to mongo
    categories()

    # load categories from mongo, return "recipes_categories"
    load_file()

    try:
        # creat threads
        worker1 = threading.Thread(target=worker, args=(
            1, web_url['icook'], recipes_categories['米食'], "rice", 0))
        worker2 = threading.Thread(target=worker, args=(
            2, web_url['icook'], recipes_categories['麵食'], "noodle", 0))
        worker3 = threading.Thread(target=worker, args=(
            3, web_url['icook'], recipes_categories['湯'], "soup", 0))
        worker4 = threading.Thread(target=worker, args=(
            4, web_url['icook'], recipes_categories['雞肉'], "chicken", 0))
        worker5 = threading.Thread(target=worker, args=(
            5, web_url['icook'], recipes_categories['牛肉'], "beef", 0))
        worker6 = threading.Thread(target=worker, args=(
            6, web_url['icook'], recipes_categories['豬肉'], "pork", 0))
        worker7 = threading.Thread(target=worker, args=(
            7, web_url['icook'], recipes_categories['羊肉'], "lamp", 0))
        worker8 = threading.Thread(target=worker, args=(
            8, web_url['icook'], recipes_categories['鴨肉'], "duck", 0))
        worker9 = threading.Thread(target=worker, args=(
            9, web_url['icook'], recipes_categories['素食'], "vegetarian", 0))
        worker10 = threading.Thread(target=worker, args=(
            10, web_url['icook'], recipes_categories['台灣小吃'], "taiwan_snacks", 0))
        
        '''
        Done
        '米食', '麵食' ,'湯' ,'雞肉' ,'牛肉' ,'豬肉' ,'羊肉' ,'鴨肉' ,'素食' ,'海鮮'

        '''

        # start threads
        worker1.start()
        worker2.start()
        worker3.start()
        worker4.start()
        worker5.start()
        worker6.start()
        worker7.start()
        worker8.start()
        worker9.start()
        worker10.start()
    except:
        print("Error: unable to start thread")


if __name__ == '__main__':
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
    client = pymongo.MongoClient(
        'mongodb://%s:%s@%s:%s/' % ('root', 'root', '114.44.74.127', '27017'))
    db = client.test

    recipes_categories = {}

    main()
