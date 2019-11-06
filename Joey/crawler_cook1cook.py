import requests, bs4, re, os, jieba, datetime, time, random, sys, traceback, json


### 建立資料夾
now_date = str(datetime.date.today())
folder_path = r"./downloads/COOK1COOK_" + now_date
if os.path.exists(folder_path)  == False:
    os.mkdir(folder_path)


my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

start_page = "https://cook1cook.com/recipe/"
recipe_num = 1
### till 47787

for i in range(1000):

    try:
        recipe_url = start_page + str(recipe_num)
        print("Recipe downloading: " + recipe_url)

        ### 取得HTML
        recipe_searched_html = requests.get(url = recipe_url, headers = my_headers)  #欲下載網址網址當參數，傳回網頁的HTML格式
        recipe_searched_html.raise_for_status()  #.raise_for_status()若目標網頁伺服器阻擋，擷取望頁內容有錯誤時，列印出原因
        recipe_searched_soup = bs4.BeautifulSoup(recipe_searched_html.text, "html.parser")  #.text是指網頁內容，lxml是較新的、解析HTML文件的方式

        ### 料理名
        dish_name = recipe_searched_soup.select('h1[itemprop="name"]')[0].text.strip()
        dish_name = re.sub(r"【.*】", "", dish_name)
        print(dish_name)


        ### 圖片
        img_url = recipe_searched_soup.select('div[class="recipe-picture-frame"] a')[0]["href"]
        # img_html = requests.get(url = img_url, headers = my_headers)
        # img_content = img_html.content
        # img_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".jpg"
        #
        # if os.path.exists(img_path) == False:
        #     with open(file = img_path, mode = "wb") as pic:
        #         pic.write(img_content)
        # else:
        #     print("Image " + str(recipe_num) + " already downloaded")


        ### 日期
        upload_date = recipe_searched_soup.select('div[class="col-xs-12"] span')[0].text
        upload_date = re.sub(r'[^0-9]*', "", upload_date)
        upload_date = datetime.datetime.strptime(upload_date, "%Y%m%d").strftime("%Y-%m-%d")
        #print(upload_date)
        #print(type(upload_date))


        ### 份數
        try:
            serving = recipe_searched_soup.select('span[itemprop = "recipeYield"]')[0].text
            serving = re.sub(r"[^0-9]*", "", serving)[0]
            serving = int(serving)
        except:
            serving = 1
        #print(serving)
        #print(type(serving))


        ### josn樣板
        single_recipe = {
            'recipe_name': dish_name,
            'recipe_url': recipe_url,
            'recipe_img_url': img_url,
            'post_time': upload_date,
            'quantity': serving,
            'ingredients': [],
            'cooking_steps': []
        }


        ### 食材與數量單位
        ingredients_list = recipe_searched_soup.select('span[class="pull-left ingredient-name"]')
        for index, ingredients_info in enumerate(ingredients_list):
            ingredients = recipe_searched_soup.select('span[class="pull-left ingredient-name"]')[index].text.strip()
            quantities = recipe_searched_soup.select('span[class="pull-right ingredient-unit"]')[index].text.strip()
            single_recipe['ingredients'].append({
                'ingredient_name': ingredients,
                'ingredient_unit': quantities
            })


        # ### 食材
        # ingredients =  recipe_searched_soup.select('span[class="pull-left ingredient-name"]')
        # ingredients_list = []
        # for i in ingredients:
        #     ingredients_list.append(i.text.strip())
        # ingredients_str = ",".join(ingredients_list)
        # #print(ingredients_str)
        #
        #
        # ### 數量單位
        # quantities = recipe_searched_soup.select('span[class="pull-right ingredient-unit"]')
        # quantities_list = []
        # for i in quantities:
        #     quantities_list.append(i.text.strip())
        # quantities_str = ",".join(quantities_list)
        # #print(quantities_str)


        ### 料理步驟
        directions_list = recipe_searched_soup.select('li[class="step"] div[class="media-body"]')
        for index, directions_info in enumerate(directions_list):
            step_num = index + 1
            directions = recipe_searched_soup.select('li[class="step"] div[class="media-body"]')[index].text.strip()
            directions = re.sub(" ", "", directions)
            directions = re.sub("\t", "", directions)
            directions = re.sub("\n", "", directions)
            directions = re.sub("\r", "", directions)
            directions = re.sub("\r\n", "", directions)
            directions = directions[1:]
            single_recipe['cooking_steps'].append({
                "steps": step_num,
                "methods": directions
            })


        # directions = recipe_searched_soup.select('li[class="step"] div[class="media-body"]')
        # directions_list = []
        # for i in directions:
        #     directions_list.append(i.text.strip())
        #
        # directions_str = ",".join(directions_list)
        # directions_str = re.sub(" ", "", directions_str)
        # directions_str = re.sub("\r\n", "", directions_str)
        # #print(directions_str)

        ### 印出結果
        # print(single_recipe)


        ### 儲存json
        json_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".json"
        if os.path.exists(json_path) == False:
            with open(file = json_path, mode = "w", encoding='utf-8') as doc:
                doc.write(json.dumps(single_recipe, ensure_ascii= False))
        else:
            print("Recipe " + str(recipe_num) + " had already downloaded")


        # ### 文字儲存
        # text_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".txt"
        # if os.path.exists(text_path) == False:
        #     with open(file = text_path, mode = "w", encoding= 'utf-8') as note:
        #         all_str = dish_name + "\n" + ingredients_str + "\n" + quantities_str +  "\n" + directions_str
        #         note.write(all_str)
        # else:
        #     print("Text " + str(recipe_num) + " already downloaded")


        print("Recipe scanned complete: " + recipe_url)
        print("======================================================================================================")
        print("")

    except Exception as err:
        error_class = err.__class__.__name__  # 取得錯誤類型
        detail = err.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = "line {}, in {}: [{}] {}".format(lineNum, funcName, error_class, detail)
        print(errMsg)
        print("Error occurred at link: " + recipe_url)
        print("======================================================================================================")
        print("")

        ### 紀錄錯誤log
        log_name = "log_" + now_date
        log_path = folder_path + "/" + log_name + ".txt"

        with open(file=log_path, mode="a", encoding='utf-8') as log:
            error_str = recipe_url + "\n" + str(errMsg) + "\n" + "*********************************************" + "\n" + "\n"
            log.write(error_str)


    ### 接續下一頁
    recipe_num = recipe_num + 1
    # time.sleep(random.randint(2,5))
