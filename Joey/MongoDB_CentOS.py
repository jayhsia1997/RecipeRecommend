import os, json, pymongo


### 更換要載入資料庫的目標時，需修改項目 dirpath, client, file_path

### 從資料夾內提起出裡面所有檔案的名稱
dirPath = r"/root/RecipeRecommend/Joey/downloads/FOODING_2019-11-07"
json_file_name_list = next(os.walk(dirPath))[2]  #index參數(dirpath, dirname, filenames)
print(json_file_name_list)
print(type(json_file_name_list))
print(len(json_file_name_list))


client = pymongo.MongoClient("mongodb://192.168.252.138:27017/")  #設定連線終端位置
db = client["foodie_test"]  #設定DataBase名稱
collection = db["fooding"]  #設定Collection名稱


###從各個json檔案內提取出裡面的內容，json檔裡面的格式就是字典
for i in json_file_name_list:
    file_path = r"/root/RecipeRecommend/Joey/downloads/FOODING_2019-11-07/" + i  #i會是每個檔案的名字
    print(file_path)
    with open(file = file_path, mode="r", encoding="utf-8") as f:
        single_recipe_dict = json.load(f)  # 提取出的內容格式是dict
        #print(single_recipe_dict)
        collection.insert_one(single_recipe_dict)
        print(single_recipe_dict['recipe_name'],":加入資料庫")