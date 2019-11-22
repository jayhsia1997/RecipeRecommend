import os, json, pymongo, datetime, time, sys


### 更換要載入資料庫的目標時，需修改項目 dirpath, client, file_path, collection
# joey a12341234 10.120.38.13

### 從資料夾內提起出裡面所有檔案的名稱
now_date = str(datetime.date.today())

# dirPath = r"./downloads/fooding_" + now_date
dirPath = r"./downloads"

for foldernames in os.listdir(dirPath):
    if foldernames.startswith("fooding"):
        folder_path = dirPath + "/" + foldernames
        print("抓取此資料夾檔案: ",folder_path)
        json_file_name_list = next(os.walk(folder_path))[2]  # index參數(dirpath, dirname, filenames)
        # print(json_file_name_list)
        # print(type(json_file_name_list))
        # print(len(json_file_name_list))

        client = pymongo.MongoClient("mongodb://%s:%s@10.120.38.13" % ("joey", "a12341234"), 27017)  # 設定連線終端位置
        db = client["food"]  # 設定DataBase名稱
        collection = db["fooding"]  # 設定Collection名稱

        ###從各個json檔案內提取出裡面的內容，json檔裡面的格式就是字典
        try:
            for i in json_file_name_list:
                file_path = folder_path + "/" + i  # i會是每個檔案的名字
                print(file_path)
                with open(file=file_path, mode="r", encoding="utf-8") as f:
                    single_recipe_dict = json.load(f)  # 提取出的內容格式是dict
                    # print(single_recipe_dict)
                    collection.insert_one(single_recipe_dict)
                    print(single_recipe_dict['recipe_name'], ":加入資料庫")
        except:
            # print(sys.exc_info())
            continue

    elif foldernames.startswith("cook1cook"):
        folder_path = dirPath + "/" + foldernames
        print("抓取此資料夾檔案: ",folder_path)
        json_file_name_list = next(os.walk(folder_path))[2]  # index參數(dirpath, dirname, filenames)
        # print(json_file_name_list)
        # print(type(json_file_name_list))
        # print(len(json_file_name_list))

        # client = pymongo.MongoClient("mongodb://%s:%s@10.120.38.13" % ("joey", "a12341234"), 27017)  # 設定連線終端位置
        # db = client["food"]  # 設定DataBase名稱
        # collection = db["cook1cook"]  # 設定Collection名稱

    else:
        continue

    print("Write into DB finished")


# json_file_name_list = next(os.walk(dirPath))[2]  #index參數(dirpath, dirname, filenames)
# print(json_file_name_list)
# print(type(json_file_name_list))
# print(len(json_file_name_list))
#
#
# client = pymongo.MongoClient("mongodb://192.168.43.8:27017/")  #設定連線終端位置
# db = client["food"]  #設定DataBase名稱
# collection = db["fooding"]  #設定Collection名稱
#
#
#
###從各個json檔案內提取出裡面的內容，json檔裡面的格式就是字典
# for i in json_file_name_list:
#     file_path = dirPath + "/" + i  #i會是每個檔案的名字
#     print(file_path)
#     with open(file = file_path, mode="r", encoding="utf-8") as f:
#         single_recipe_dict = json.load(f)  # 提取出的內容格式是dict
#         #print(single_recipe_dict)
#         collection.insert_one(single_recipe_dict)
#         print(single_recipe_dict['recipe_name'],":加入資料庫")




