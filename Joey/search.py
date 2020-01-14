import os, json, pymongo, datetime, time, sys, pandas as pd, MySQLdb
from sqlalchemy import create_engine, Column, Integer, String, FLOAT, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import pymongo, pandas as pd


myclient = pymongo.MongoClient(host="mongodb://{}:{}@220.129.16.234" .format("user", "user"), port=27017)  # 設定連線終端位置
mydb = myclient["test"]  # 設定DataBase名稱
mycol = mydb["food"]  # 設定Collection名稱
df = pd.read_csv("./merge.csv")  #熱量對照表來源
sdf= pd.DataFrame(columns=['name','ID','unit_overall','unit_fc','calories_kcal','protein_g','fat_g','carbohydrate_g',
    'dietary_fiber_g','sugar_g','vitamin_c_mg','vitamin_a_ug','vitamin_e_mg','vitamin_b1_mg','vitamin_b2_mg','vitamin_b6_mg',
    'vitamin_b12_ug','sodium_mg','potassium_mg','calcium_mg','magnesium_mg','iron_mg','zinc_mg','phosphorus_mg',
    'nicotinin_mg','folate_ug','alpha_carotene_ug','beta_carotene_ug','saturated_fat_g','water_g','ash_g'])

def mutiply (x):  #提供各食材的份數，乘上每單位營養值。
    x = round(quantity * x, 2)
    return x

def re_name (x):  #pandas的apply函式到df，需搭配funciton，回傳mongo的食譜名稱。
    x = recipe_name
    return x

def re_id (x):  #pandas的apply函式到df，需搭配funciton，回傳mongodb的食譜id。
    x = num
    return x

for i in range(6429):
    num = 29102  #給予查詢的食譜id
    num= i+num
    print(i)
    print(num)
    single_recipe = mycol.find_one({"_id":num})  #從mongo抓出食譜
    ingredients = single_recipe["ingredients"]  #食譜中透過key去得到食材的value，格式會是list包著dict
    recipe_name = single_recipe["recipe_name"]  #食譜中透過key去得到食譜名稱的value
    print(recipe_name)

    for index, dict in enumerate (ingredients):
        # print(dict)
        name = dict["ingredient_names"]
        unit = dict["ingredient_units"]
        try:
            quantity = float(dict["ingredient_quantity"])  #將食材份數轉為float，才可與營養值df的各欄位值相乘
        except:
            quantity = 1  #假設取出的食材份數有問題(可能非數字，則直接給予數量1做取代)
        filter1 = (df['name'] == name)  #用於搜尋營養值df內的某筆資料，第一個條件為搜尋食材名稱
        filter2 = (df['unit_overall'] == unit)  #用於搜尋營養值df內的某筆資料，第二個條件為搜尋食材單位
        search = df[filter1 & filter2]  #合併搜尋條件後，執行搜尋，回傳符合此條件的食材營養資料
        for index, col in enumerate(search):
            if index == 0:
                search[col] = search[col].apply(re_name)  #第一欄原為食材名稱，更改為食譜名稱
            elif index == 1:
                search[col] = search[col].apply(re_id)  #第二欄原為食材id，更改為食譜id。
            elif index == 2:
                search[col] = search[col].apply(re_name)  #第三欄原為食材單位(字串格式)，更改為食譜名稱。
            else:
                search[col] = search[col].apply(mutiply)  #其餘欄位原為該單位營養值，直接乘上食材份數，得到該食材的總營養值。
        # print(search)


        sdf = sdf.append(pd.DataFrame(search, columns=['name','ID','unit_overall','unit_fc','calories_kcal','protein_g',
            'fat_g','carbohydrate_g','dietary_fiber_g','sugar_g','vitamin_c_mg','vitamin_a_ug','vitamin_e_mg','vitamin_b1_mg',
            'vitamin_b2_mg','vitamin_b6_mg','vitamin_b12_ug','sodium_mg','potassium_mg','calcium_mg','magnesium_mg',
            'iron_mg','zinc_mg','phosphorus_mg','nicotinin_mg','folate_ug','alpha_carotene_ug','beta_carotene_ug',
            'saturated_fat_g','water_g','ash_g']))
            #將每個食譜的每筆食材的營養值，依序寫入新的df內。

    print("-----------------------------------------")


# print(sdf)
sdf = sdf.groupby(['ID','name']).sum()  #將新的整份df內的所有的食材的營養值，透過同個食譜名稱與ID，合併起來成為單一食譜的營養值。
print(sdf)
sdf.to_csv('C:/Users/CYC/Desktop/recipes.csv',)  #將新的df寫成一份csv檔輸出。











#------------------------------------------------------
# mysql = MySQLdb.connect(host = "114.44.77.36",port=3306, user="user", passwd="user", db= "iii_project", charset="utf8")
# cursor = mysql.cursor()
# sql_str = "SELECT * from merge_final;"
# cursor.execute(sql_str)
# datarows = cursor.fetchall()
# print(type(datarows))
# for row in datarows:
#     print(type(row))
#     print(row)

# ---------------------------------------
# myengine = create_engine("mysql+pymysql://user:user@114.44.77.36:3306/iii_project", echo=False)
# DBsession = sessionmaker(bind=myengine)
# session = DBsession()
#
# base = declarative_base()
# class table(base):
#     __tablename__ = "merge_final"
#     name = Column(String)
#     unit = Column(String)
#
# session.query(table)

# connection = myengine.connect()
# result = connection.execute("SELECT * FROM iii_project.merge_final;")
# print(result)


# print(myengine)


# dataframe = pandas.read_sql_query('SELECT * FROM iii_project.merge_final;', myengine)
# dataframe.head(2)