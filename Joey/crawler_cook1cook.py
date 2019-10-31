import requests, bs4, re, os, jieba, datetime, time, random

###建立資料夾
now_date = str(datetime.date.today())
folder_path = r"./downloads/COOK1COOK_" + now_date
if os.path.exists(folder_path)  == False:
    os.mkdir(folder_path)


my_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

start_page = "https://cook1cook.com/recipe/"
recipe_num = 47788
### till 47787

for i in range(1):

    try:
        recipe_url = start_page + str(recipe_num)
        print("Recipe downloading: " + recipe_url)

        ###取得HTML
        recipe_searched_html = requests.get(url = recipe_url, headers = my_headers)  #欲下載網址網址當參數，傳回網頁的HTML格式
        recipe_searched_html.raise_for_status()  #.raise_for_status()若目標網頁伺服器阻擋，擷取望頁內容有錯誤時，列印出原因
        recipe_searched_soup = bs4.BeautifulSoup(recipe_searched_html.text, "html.parser")  #.text是指網頁內容，lxml是較新的、解析HTML文件的方式

        ###料理名
        dish = recipe_searched_soup.select('h1[itemprop="name"]')[0]
        dish_name = dish.text.strip()
        print(dish_name)

        ###食材
        ingredients =  recipe_searched_soup.select('span[class="pull-left ingredient-name"]')
        ingredients_list = []
        for i in ingredients:
            ingredients_list.append(i.text.strip())
        ingredients_str = ",".join(ingredients_list)
        #print(ingredients_str)

        ###數量單位
        quantities = recipe_searched_soup.select('span[class="pull-right ingredient-unit"]')
        quantities_list = []
        for i in quantities:
            quantities_list.append(i.text.strip())
        quantities_str = ",".join(quantities_list)
        #print(quantities_str)

        ###料理步驟
        directions = recipe_searched_soup.select('li[class="step"] div[class="media-body"]')
        directions_list = []
        for i in directions:
            directions_list.append(i.text.strip())

        directions_str = ",".join(directions_list)
        directions_str = re.sub(" ", "", directions_str)
        directions_str = re.sub("\r\n", "", directions_str)
        #print(directions_str)

        # print("1",directions_str)
        # print("1",type(directions_str))
        # directions_str = re.sub(r" ", "", directions_str)
        # print("2", directions_str)
        # print("2",type(directions_str))
        # directions_str = directions_str.split("+")
        # print("3", directions_str)
        # print("3", type(directions_str))
        # directions_str = "!!!".join(directions_str)
        # print("4", directions_str)
        # print("4", type(directions_str))
        # print(directions_str)

        ###文字儲存
        text_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".txt"
        if os.path.exists(text_path) == False:
            with open(file = text_path, mode = "w", encoding= 'utf-8') as note:
                all_str = dish_name + "\n" + ingredients_str + "\n" + quantities_str +  "\n" + directions_str
                note.write(all_str)
        else:
            print("Text " + str(recipe_num) + " already downloaded")


        ###圖片
        img_url = recipe_searched_soup.select('div[class="recipe-picture-frame"] a')[0]["href"]
        img_html = requests.get(url = img_url, headers = my_headers)
        img_content = img_html.content
        img_path = folder_path + "/" + str(recipe_num) + "_" + dish_name + ".jpg"

        if os.path.exists(img_path) == False:
            with open(file = img_path, mode = "wb") as pic:
                pic.write(img_content)
        else:
            print("Image " + str(recipe_num) + " already downloaded")

        print("Recipe download complete: " + recipe_url)
        print("======================================================================================================")
        print("")

    except Exception as err:
        print("Error occurred at link: " + recipe_url)
        print(str(err))

        ###紀錄錯誤log
        log_name = "log_" + now_date
        log_path = folder_path + "/" + log_name + ".txt"

        with open(file=log_path, mode="a", encoding='utf-8') as log:
            error_str = recipe_url + "\n" + str(err) + "\n" + "*********************************************" + "\n" + "\n"
            log.write(error_str)



    ###接續下一頁
    recipe_num = recipe_num + 1
    # time.sleep(random.randint(2,5))
