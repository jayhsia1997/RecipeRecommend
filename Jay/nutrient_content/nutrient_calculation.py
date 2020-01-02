# -*- coding: utf-8 -*-

import time
import pymongo
import sys
import os
import json
import re
import MySQLdb as mysql
# --------------------------------------------------------------------------------------------------

def load_file():
    '''
    Done
    beef, chicken, duck, lamp, noodle, pork, rice, soup, taiwan_snacks(id=619), vegetarian, japanese_cuisine(id=899), korean_cuisine, 
    thai_cuisine, italian_cuisine, hongkong_cuisine, french_cuisine, curry, baked, low_calories, stir_fried
    
    Not done
    
    read_categories = mongo_db.taiwan_snacks.find({"_id":620})
    '''
    try:
        read_categories = mongo_db..find()
        for i, temp in enumerate(read_categories):
            print(i+1)
            for j, temp2 in enumerate(temp['ingredients']):
                # print(temp2['ingredient_name'])
                val = re.sub(r'[^\u4e00-\u9fa5]', '', temp2['ingredient_name'])
                sql_insert = "INSERT INTO iii_project.ingredient_names (ingredient_name) VALUES('%s')" % (val)
                cursor.execute(sql_insert)
                mysql_db.commit()
    except:
        print(sys.exc_info())
    # print(len(recipes_categories))

def main():
    # load_file()
    
    
if __name__ == "__main__":
    # mongo connect set
    client = pymongo.MongoClient(
        'mongodb://%s:%s@%s:%s/' % ('root', 'root', '114.44.69.179', '27017'))
    mongo_db = client.test
    # mysql connect set
    mysql_db = mysql.connect(host = '36.228.69.179', user = 'root', passwd = 'root', port = 3306, charset = 'utf8')
    cursor = mysql_db.cursor()
    
    main()