# -*- coding: utf-8 -*-

import time
import pymongo
import sys
import json
import re
# --------------------------------------------------------------------------------------------------

def load_file():
    collections = ['beef', 'chicken', 'duck', 'lamp', 'noodle', 'pork', 'rice', 'soup', 'taiwan_snacks', 
                   'vegetarian', 'japanese_cuisine', 'korean_cuisine', 'thai_cuisine', 'italian_cuisine', 
                   'hongkong_cuisine', 'french_cuisine', 'curry', 'baked', 'low_calories', 'stir_fried']
    
    recipe_id = 29102

    try:
        '''
        for x, collections_list in enumerate(collections):
            mongo_db = client.test
            read_mongo = mongo_db.food2.find_one()
            for i, temp in enumerate(read_mongo):
                print(temp)
                temp['_id'] = recipe_id
                mongo_db = client.test
                mongo_db.recipes.insert_one(temp)
                recipe_id += 1
        '''
        mongo_db = client.test
        clear_up_ingredients = {}
        clear_up_cooking_steps = {}
        clear_up_ingredients['ingredients'] = []
        clear_up_cooking_steps['cooking_steps'] = []
        # read_mongo = mongo_db.food.aggregate([{'$sample':{'size':200}}])
        # read_mongo = mongo_db.food.find({'_id':{'$lte':29111}})
        read_mongo = mongo_db.food.find()
        for i, temp in enumerate(read_mongo):
            print(temp['_id'])
            for j, ingredients in enumerate(temp['ingredients']):
                raw_ingredient_name = ingredients['ingredient_names']
                raw_ingredient_quantity = ingredients['ingredient_quantity']
                raw_ingredient_unit = ingredients['ingredient_units']
                clear_up_ingredients['ingredients'].append({
                    'ingredient_name': raw_ingredient_name,
                    'ingredient_quantity': raw_ingredient_quantity,
                    'ingredient_unit': raw_ingredient_unit})
                
            for j, steps in enumerate(temp['cooking_steps']):
                raw_steps = steps['steps']
                raw_methods = steps['methods']
                clear_up_cooking_steps['cooking_steps'].append({
                    'steps': raw_steps,
                    'methods': raw_methods,})
            
            temp = {'_id': temp['_id'],
                    'recipe_name': temp['recipe_name'],
                    'recipe_url': temp['recipe_url'],
                    'recipe_img_url': temp['recipe_img_url'],
                    'post_time': temp['post_time'],
                    'quantity': temp['quantity'],
                    'ingredients': [],
                    'cooking_steps': []}
            
            temp['ingredients'] = clear_up_ingredients['ingredients']
            temp['cooking_steps'] = clear_up_cooking_steps['cooking_steps']
            # print(temp)
            mongo_db.clear_up_recipes.insert_one(temp)
            clear_up_ingredients['ingredients'] = []
            clear_up_cooking_steps['cooking_steps'] = []
    except:
        print(sys.exc_info())
        
def load_file2():
    mongo_db = client.test
    clear_up_ingredients = {}
    clear_up_ingredients['ingredients'] = []
    try:
        # temp = mongo_db.recipes.aggregate([{'$sample':{'size':200}}])
        # temp = mongo_db.recipes.find({'_id':{'$lte':20}})
        # temp = mongo_db.recipes.find({'_id':1})
        temp = mongo_db.recipes.find()
        for i, recipes_data in enumerate(temp):
            print(recipes_data['_id'])
            if recipes_data['ingredients'] != []:
                for j, ingredients in enumerate(recipes_data['ingredients']):
                    # print(recipes_data['ingredients'][j])
                    raw_ingredient_name = ingredients['ingredient_name']
                    raw_ingredient_quantity = re.split(r'[\u4e00-\u9fa5a-zA-Z]', ingredients['ingredient_unit'].split('(')[0].split('（')[0].replace(' ',''))
                    raw_ingredient_unit = re.split(r'[^\u4e00-\u9fa5a-zA-Z]', ingredients['ingredient_unit'].split('(')[0].split('（')[0])
                    for x in range(len(raw_ingredient_quantity)):
                        ingredient_quantity = None
                        if raw_ingredient_quantity[x] != '':
                            ingredient_quantity = raw_ingredient_quantity[x]
                            if ingredient_quantity == '.':
                                ingredient_quantity = None
                            if ingredient_quantity != None:
                                break
                                                        
                    if raw_ingredient_unit[-1] != '':
                        ingredient_units = raw_ingredient_unit[-1]        
                    elif raw_ingredient_unit[-1] == '':
                        ingredient_units = None
                        
                    clear_up_ingredients['ingredients'].append({
                        'ingredient_name': raw_ingredient_name,
                        'ingredient_quantity': ingredient_quantity,
                        'ingredient_unit': ingredient_units})
                    
            recipes_data['ingredients'] = []
            recipes_data['ingredients'] = clear_up_ingredients['ingredients']
            # print(recipes_data)
            mongo_db.clear_up_recipes.insert_one(recipes_data)
            clear_up_ingredients['ingredients'] = []
    except:
        print(sys.exc_info())
        pass

def main():
    load_file()
    # load_file2()
    
if __name__ == "__main__":
    # mongo connect set
    client = pymongo.MongoClient(
        'mongodb://%s:%s@%s:%s/' % ('root', 'root', '114.44.77.36', '27017'))
    
    main()