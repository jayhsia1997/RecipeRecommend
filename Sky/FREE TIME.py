import requests
from bs4 import BeautifulSoup
import os
import time

user_agenttt="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
headers={"user-agent":user_agenttt,
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
"cache-control": "no-cache",
"pragma": "no-cache",
"referer": "https://food.ltn.com.tw/article/9373",
"sec-fetch-mode": "nested-navigate",
"sec-fetch-site": "cross-site",
"upgrade-insecure-requests": "1"}

path=r'./food'
if not os.path.exists(path):
    os.mkdir(path)

list_of_recipe=[]
url_first="https://food.ltn.com.tw/category"
res_first = requests.get(url_first, headers=headers)
soup_first = BeautifulSoup(res_first.text, 'html.parser')
titles_first = soup_first.select('p')
for title_first in titles_first:
    try:
        if (title_first.a["href"] != "type/84") and (title_first.a["href"] != "type/87") and (title_first.a["href"] != "type/243"):
            url_second_level= "https://food.ltn.com.tw/" + title_first.a["href"] + "/" + str(1)
            res_second = requests.get(url_second_level, headers=headers)
            soup_second = BeautifulSoup(res_second.text, 'html.parser')
            page_tail=soup_second.select('a[class="p_last"]')
            page_last_number = page_tail[0]['href'].split("/")[5]
            page_number=1
            while page_number <= int(page_last_number):
                url_second_level_every_page = "https://food.ltn.com.tw/" + title_first.a["href"]+"/"+str(page_number)
                res_second_every_page = requests.get(url_second_level_every_page, headers=headers)
                soup_second_every_page = BeautifulSoup(res_second_every_page.text, 'html.parser')
                url_thrds = soup_second_every_page.select('div[data-desc="清單"] a')
                print(str(page_number)+"page"+"~~~~~~~~~~~~~~~~~~~")
                Dict_for_a_recipe={}
                for url_thrd in url_thrds:
                    url_third_level="https://food.ltn.com.tw/"+url_thrd["href"]
                    Dict_for_a_recipe["recipe_url"]=url_third_level
                    res_third = requests.get(url_third_level, headers=headers)
                    soup_third = BeautifulSoup(res_third.text, 'html.parser')
                    print("~~~~~~~~~~~~~~~~~~the_third_level~~~~~~~~~~~~~~~~~~~~~")
                    try:
                        food_titles=soup_third.select('div[data-desc="內容頁"] h1')
                        food_title=food_titles[0].text
                        Dict_for_a_recipe["recipe_name"]=food_title
                        image_links = soup_third.select('div[class="print_re"] img')
                        image_link=image_links[0]["src"]
                        Dict_for_a_recipe["recipe_img_url"]=image_link
                        times = soup_third.select('span[class="author"] b')
                        time=times[0].text
                        time=time.replace("/","-")
                        Dict_for_a_recipe["post_time"]=time
                        Dict_for_a_recipe["quantity"]="1份"
                        ingredients = soup_third.select('dl[class="recipe"] dd')
                        list_of_ingredients = []
                        for i in ingredients:
                            x=i.text.split("\n")
                            for ingredient in x:
                                d = {}
                                d["ingredient_names"]=ingredient
                                d["ingredient_units"]="1"
                                list_of_ingredients.append(d)
                        Dict_for_a_recipe["ingredients"]=list_of_ingredients
                        steps = soup_third.select('div[class="word"]')
                        list_of_steps=[{"steps":n+1,"methods":step.p.text} for n,step in enumerate(steps) ]
                        Dict_for_a_recipe["cooking_steps"]=list_of_steps
                        list_of_recipe.append(Dict_for_a_recipe)
                    except IndexError as e:
                        print(e)

                print(list_of_recipe)

                page_number += 1
    except TypeError as e:
        print(e)


json={}
json["recipe"]=list_of_recipe
with open('FOOD.txt', 'w', encoding='utf-8') as f:
    f.write(json)



