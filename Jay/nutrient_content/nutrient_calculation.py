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
    try:
        read_categories = mongo_db.chicken.find()
        for i, temp in enumerate(read_categories):
            print(i)
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
    load_file()
    
    
if __name__ == "__main__":
    # mongo connect set
    client = pymongo.MongoClient(
        'mongodb://%s:%s@%s:%s/' % ('root', 'root', '114.44.74.127', '27017'))
    mongo_db = client.test
    # mysql connect set
    mysql_db = mysql.connect(host = '114.44.74.127', user = 'root', passwd = 'root', port = 3306, charset = 'utf8')
    cursor = mysql_db.cursor()
    
    main()