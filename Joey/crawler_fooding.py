import requests, bs4, re, os, jieba, datetime, time, random


### 建立資料夾
now_date = str(datetime.date.today())
folder_path = r"./downloads/FOODING_" + now_date
if os.path.exists(folder_path)  == False:
    os.mkdir(folder_path)


my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

start_page = "https://www.fooding.com.tw/recipe-shares.php?cookid="
recipe_num = 100001
### till 116124

for i in range(1):

    try:
        recipe_url = start_page + str(recipe_num)
        print("Recipe downloading: " + recipe_url)

        ### 取得HTML
        recipe_searched_html = requests.get(url = recipe_url, headers = my_headers)  #欲下載網址網址當參數，傳回網頁的HTML格式
        recipe_searched_html.raise_for_status()  #.raise_for_status()若目標網頁伺服器阻擋，擷取望頁內容有錯誤時，列印出原因
        recipe_searched_soup = bs4.BeautifulSoup(recipe_searched_html.text, "html.parser")  #.text是指網頁內容，lxml是較新的、解析HTML文件的方式

        json_recipe = {}
        json_recipe["recipe"] = []
        json_ingredients = ""

        ### 料理名
        dish_name = recipe_searched_soup.select('ol[class="breadcrumb"] li')[2].text
        # dish_name = recipe_searched_soup.select('form[class="form-horizontal"]')[0].h1.text
        # dish_name = re.sub(r"【.*】", "", dish_name)
        print(dish_name)

        ### 日期
        upload_date = recipe_searched_soup.select('h4[class="panel-title"] small')[0].text
        upload_date = datetime.datetime.strptime(upload_date, "%Y/%m/%d").strftime("%Y-%m-%d")
        print(upload_date)

        ### 食材
        ingredients =  recipe_searched_soup.select('div[class="row mg-btm10-border"] div[class="col-sm-8"]')
        ingredients_list = []
        for i in ingredients:
            ingredients_list.append(i.text)
        ingredients_str = ",".join(ingredients_list)
        #print(ingredients_str)

        ### 數量單位
        quantities = recipe_searched_soup.select('div[class="col-sm-4 text-right"]')
        quantities_list = []
        for i in quantities:
            quantities_list.append(i.text)
        quantities_str = ",".join(quantities_list)
        #print(quantities_str)

        ### 料理步驟
        directions = recipe_searched_soup.select('div[class="row mg-btm10"] p')
        directions_list = []
        for i in directions:
            directions_list.append(i.text)
        directions_str = ",".join(directions_list)
        #print(directions_str)

        # 儲存json

        {"recipe": [{"recipe_name": "【厚生廚房】黑豆麻油雞飯", "recipe_url": "https://icook.tw/recipes/313912",
                     "recipe_img_url": "https://tokyo-kitchen.icook.network/uploads/recipe/cover/313912/small_cba28d103faf8a8e.jpg",
                     "ingredients": [{"ingredient_name": "黑豆茶(乾-已經過烘焙)", "ingredient_unit": "1/4杯"},
                                     {"ingredient_name": "去骨雞腿", "ingredient_unit": "280克"},
                                     {"ingredient_name": "白米", "ingredient_unit": "2杯"},
                                     {"ingredient_name": "黑芝麻油", "ingredient_unit": "2大匙"},
                                     {"ingredient_name": "老薑", "ingredient_unit": "8-10片"},
                                     {"ingredient_name": "鹽", "ingredient_unit": "適量"},
                                     {"ingredient_name": "米酒", "ingredient_unit": "1/2杯"}]}]}



        #
        # full_recipe.append(
        #     {
        #     "recipe_name": recipe_name,
        #     "recipe_url": recipe_url,
        #     "recipe_img_url": recipe_img,
        #     "ingredients": []
        # })



        # ### 文字儲存
        # text_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".txt"
        # if os.path.exists(text_path) == False:
        #     with open(file = text_path, mode = "w", encoding= 'utf-8') as note:
        #         all_str = dish_name + "\n" + ingredients_str + "\n" + quantities_str +  "\n" + directions_str
        #         note.write(all_str)
        # else:
        #     print("Text " + str(recipe_num) + " already downloaded")
        #
        # ### 圖片
        # img_url = recipe_searched_soup.select('label[class="col-sm-7 control-label"] img')[0]["src"]
        # img_html = requests.get(url = img_url, headers = my_headers)
        # img_content = img_html.content
        # img_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".jpg"
        #
        # if os.path.exists(img_path) == False:
        #     with open(file = img_path, mode = "wb") as pic:
        #         pic.write(img_content)
        # else:
        #     print("Image " + str(recipe_num) + " already downloaded")

        print("Recipe download complete: " + recipe_url)
        print("======================================================================================================")
        print("")

    except Exception as err:
        print("Error occurred at link: " + recipe_url)
        print(str(err))

        #紀錄錯誤log
        log_name = "log_" + now_date
        log_path = folder_path + "/" + log_name + ".txt"

        with open(file=log_path, mode="a", encoding='utf-8') as log:
            error_str = recipe_url + "\n" + str(err) + "\n" + "*********************************************" + "\n" + "\n"
            log.write(error_str)



    #接續下一頁
    recipe_num = recipe_num + 1
    # time.sleep(random.randint(2,5))