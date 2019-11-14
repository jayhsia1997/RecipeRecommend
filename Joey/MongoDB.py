import os, json, pymongo


### 更換要載入資料庫的目標時，需修改項目 dirpath, client, file_path

### 從資料夾內提起出裡面所有檔案的名稱
dirPath = r"D:/Big_Data/fit_foodie/RecipeRecommend/Joey/downloads/FOODING_2019-11-08"
json_file_name_list = next(os.walk(dirPath))[2]  #index參數(dirpath, dirname, filenames)
print(json_file_name_list)
print(type(json_file_name_list))
print(len(json_file_name_list))


client = pymongo.MongoClient("mongodb://192.168.43.8:27017/")  #設定連線終端位置
db = client["foodie_test"]  #設定DataBase名稱
collection = db["fooding"]  #設定Collection名稱


###從各個json檔案內提取出裡面的內容，json檔裡面的格式就是字典
for i in json_file_name_list:
    file_path = r"D:/Big_Data/fit_foodie/RecipeRecommend/Joey/downloads/FOODING_2019-11-08/" + i  #i會是每個檔案的名字
    print(file_path)
    with open(file = file_path, mode="r", encoding="utf-8") as f:
        single_recipe_dict = json.load(f)  # 提取出的內容格式是dict
        #print(single_recipe_dict)
        collection.insert_one(single_recipe_dict)
        print(single_recipe_dict['recipe_name'],":加入資料庫")




### 一次多筆丟法範例
# list = [
# {"recipe_name": "好吃2 豆腐之道─和風豆腐沙拉", "recipe_url": "https://www.fooding.com.tw/recipe-shares.php?cookid=100001", "recipe_img_url": "https://fooding-aws.hmgcdn.com/images/cookbooks/100001/c100001_1370854216_c.jpg", "post_time": "2013-06-10", "quantity": 1, "ingredients": [{"ingredient_name": "嫩豆腐", "ingredient_unit": "2塊"}, {"ingredient_name": "番茄", "ingredient_unit": "2塊"}, {"ingredient_name": "西生菜", "ingredient_unit": "數片"}, {"ingredient_name": "小黃瓜", "ingredient_unit": "2 條"}, {"ingredient_name": "芽菜", "ingredient_unit": "1盒"}, {"ingredient_name": "白芝麻", "ingredient_unit": "少許"}, {"ingredient_name": "醬油", "ingredient_unit": "2大匙"}, {"ingredient_name": "醋", "ingredient_unit": "2小匙"}, {"ingredient_name": "糖", "ingredient_unit": "1小匙"}, {"ingredient_name": "油", "ingredient_unit": "1大匙"}], "cooking_steps": [{"steps": 1, "methods": "豆腐瀝乾水分，切成粗條；番茄切片；小黃瓜斜切成粗條。"}, {"steps": 2, "methods": "西生菜剝成大片，放入冰水中冰鎮5?10分鐘後，撈起瀝乾水分。"}, {"steps": 3, "methods": "將蔬菜混和鋪入盤中，再放上豆腐，淋入混合後的調味料。"}, {"steps": 4, "methods": "最後撒上芽菜和白芝麻即可。"}]},
# {"recipe_name": "好吃2 豆腐之道─鍋貼豆腐", "recipe_url": "https://www.fooding.com.tw/recipe-shares.php?cookid=100002", "recipe_img_url": "https://fooding-aws.hmgcdn.com/images/cookbooks/100002/c100002_1370855124_c.jpg", "post_time": "2013-06-10", "quantity": 1, "ingredients": [{"ingredient_name": "板豆腐", "ingredient_unit": "2塊"}, {"ingredient_name": "蔥花", "ingredient_unit": "2支"}, {"ingredient_name": "豬絞肉", "ingredient_unit": "200克"}, {"ingredient_name": "醃料：薑汁", "ingredient_unit": "少許"}, {"ingredient_name": "醃料：酒", "ingredient_unit": "1 大匙"}, {"ingredient_name": "醃料：鹽", "ingredient_unit": "1/4小匙"}, {"ingredient_name": "醃料：糖", "ingredient_unit": "1/2小匙"}, {"ingredient_name": "醃料：太白粉", "ingredient_unit": "1小匙"}, {"ingredient_name": "高湯", "ingredient_unit": "3/4杯"}, {"ingredient_name": "醬油", "ingredient_unit": "1又1/2大匙"}, {"ingredient_name": "糖", "ingredient_unit": "2小匙"}, {"ingredient_name": "太白粉", "ingredient_unit": "2小匙"}], "cooking_steps": [{"steps": 1, "methods": "豆腐瀝乾水分，切成1.5cm厚片，再用紙巾吸掉水分。"}, {"steps": 2, "methods": "將絞肉和醃料混合拌勻，沾上少許太白粉，均勻鋪在豆腐上。"}, {"steps": 3, "methods": "炒鍋以2大匙油熱鍋，以肉面朝下的方式，將豆腐放入鍋中，火可以開大些，待略呈金黃色再翻面。"}, {"steps": 4, "methods": "將調味料調勻入鍋中略煮，熄火盛盤，並撒上蔥花即可食用。"}]}
#     ]
# x = collection.insert_many(list)

###　單個key:value包住多筆丟法範例
# list = {"recipe":[
# {"recipe_name": "好吃2 豆腐之道─和風豆腐沙拉", "recipe_url": "https://www.fooding.com.tw/recipe-shares.php?cookid=100001", "recipe_img_url": "https://fooding-aws.hmgcdn.com/images/cookbooks/100001/c100001_1370854216_c.jpg", "post_time": "2013-06-10", "quantity": 1, "ingredients": [{"ingredient_name": "嫩豆腐", "ingredient_unit": "2塊"}, {"ingredient_name": "番茄", "ingredient_unit": "2塊"}, {"ingredient_name": "西生菜", "ingredient_unit": "數片"}, {"ingredient_name": "小黃瓜", "ingredient_unit": "2 條"}, {"ingredient_name": "芽菜", "ingredient_unit": "1盒"}, {"ingredient_name": "白芝麻", "ingredient_unit": "少許"}, {"ingredient_name": "醬油", "ingredient_unit": "2大匙"}, {"ingredient_name": "醋", "ingredient_unit": "2小匙"}, {"ingredient_name": "糖", "ingredient_unit": "1小匙"}, {"ingredient_name": "油", "ingredient_unit": "1大匙"}], "cooking_steps": [{"steps": 1, "methods": "豆腐瀝乾水分，切成粗條；番茄切片；小黃瓜斜切成粗條。"}, {"steps": 2, "methods": "西生菜剝成大片，放入冰水中冰鎮5?10分鐘後，撈起瀝乾水分。"}, {"steps": 3, "methods": "將蔬菜混和鋪入盤中，再放上豆腐，淋入混合後的調味料。"}, {"steps": 4, "methods": "最後撒上芽菜和白芝麻即可。"}]},
# {"recipe_name": "好吃2 豆腐之道─鍋貼豆腐", "recipe_url": "https://www.fooding.com.tw/recipe-shares.php?cookid=100002", "recipe_img_url": "https://fooding-aws.hmgcdn.com/images/cookbooks/100002/c100002_1370855124_c.jpg", "post_time": "2013-06-10", "quantity": 1, "ingredients": [{"ingredient_name": "板豆腐", "ingredient_unit": "2塊"}, {"ingredient_name": "蔥花", "ingredient_unit": "2支"}, {"ingredient_name": "豬絞肉", "ingredient_unit": "200克"}, {"ingredient_name": "醃料：薑汁", "ingredient_unit": "少許"}, {"ingredient_name": "醃料：酒", "ingredient_unit": "1 大匙"}, {"ingredient_name": "醃料：鹽", "ingredient_unit": "1/4小匙"}, {"ingredient_name": "醃料：糖", "ingredient_unit": "1/2小匙"}, {"ingredient_name": "醃料：太白粉", "ingredient_unit": "1小匙"}, {"ingredient_name": "高湯", "ingredient_unit": "3/4杯"}, {"ingredient_name": "醬油", "ingredient_unit": "1又1/2大匙"}, {"ingredient_name": "糖", "ingredient_unit": "2小匙"}, {"ingredient_name": "太白粉", "ingredient_unit": "2小匙"}], "cooking_steps": [{"steps": 1, "methods": "豆腐瀝乾水分，切成1.5cm厚片，再用紙巾吸掉水分。"}, {"steps": 2, "methods": "將絞肉和醃料混合拌勻，沾上少許太白粉，均勻鋪在豆腐上。"}, {"steps": 3, "methods": "炒鍋以2大匙油熱鍋，以肉面朝下的方式，將豆腐放入鍋中，火可以開大些，待略呈金黃色再翻面。"}, {"steps": 4, "methods": "將調味料調勻入鍋中略煮，熄火盛盤，並撒上蔥花即可食用。"}]}
#     ]}
# x = collection.insert_one(list)
# print(x.inserted_ids)