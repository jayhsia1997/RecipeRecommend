#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os,json
#MAC可能會有路徑斜線相反問題，在開檔那邊

#食譜資料夾位置
path=r"F:\資策會\專題\爬蟲\venv\collction_freefood_11_23"


# In[4]:


# 讀取json_步驟，黏合返回list
def read_from_json_step(path):
    json_list = os.listdir(path)
    list_for_steps=[]
    for i in json_list:
        with open(path + "/" + i, "r", encoding="utf-8") as f:
            dic = f.read()
            d = json.loads(dic)
            list_steps = d["cooking_steps"]
            #結合每個步驟
            s=""
            for i in list_steps:
                step=i["methods"]
                s+=step
            #去掉空行，一個食譜步驟放入一次
            list_for_steps.append(s.replace("\n",""))
            
    #return list_for_steps
    #print(list_for_steps)


# In[7]:


# 讀取json_食材_數量單位
def read_from_json_food_name_unit(path):
    json_list = os.listdir(path)
    for i in json_list:
        with open(path + "/" + i, "r", encoding="utf-8") as f:
            dic = f.read()
            d = json.loads(dic)
            list_ingredients = d["ingredients"]
            for i in list_ingredients:
                #讀每筆食材
                ingredient_names = i["ingredient_names"]
                #print(ingredient_names)
                
                #讀每筆數量與單位
                ingredient_units=i["ingredient_units"]
                #print(ingredient_names)


# In[8]:


if __name__ == "__main__":
    #read_from_json_step(path)
    #read_from_json_food_name_unit(path)

