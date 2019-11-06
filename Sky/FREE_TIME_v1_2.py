from bs4 import BeautifulSoup
import multiprocessing as mp
import os,time,random,requests,json,re
#五穀、肉
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

path1=r'./food'  #資料夾
path2=r'./collction'
if not os.path.exists(path2): #沒有這個資料夾就新創資料夾
    os.mkdir(path2)

def producer(queue):
    list_txt=os.listdir(path1) #返回path指定的文件夹包含的文件或文件夹的名字的列表
    for txt in list_txt:
        with open(path1+"/"+txt, 'r', encoding='utf-8') as f:
            str_of_class=f.read()
            list_of_class=str_of_class.split(",")
            for i in list_of_class:
                queue.put(i)
def worker(worker_id,queue):
    while True:
        no_article_thrd=queue.get()
        article_thrd="article/"+str(no_article_thrd)
        url_third_level = "https://food.ltn.com.tw/" + article_thrd
        Dict_for_a_recipe={}
        #食譜連結
        Dict_for_a_recipe["recipe_url"] = url_third_level
        # 第三層
        res_third = requests.get(url_third_level, headers=headers)
        soup_third = BeautifulSoup(res_third.text, 'html.parser')
        print("~~~~~~~~~~~~~~~~~~the_third_level~~~~~~~~~~~~~~~~~~~~~")
        try:
            # 料理名
            food_titles = soup_third.select('div[data-desc="內容頁"] h1')
            food_title = food_titles[0].text
            Dict_for_a_recipe["recipe_name"] = food_title
            # 圖片連結
            image_links = soup_third.select('div[class="print_re"] img')
            image_link = image_links[0]["src"]
            Dict_for_a_recipe["recipe_img_url"] = image_link
            # 發文時間
            times = soup_third.select('span[class="author"] b')
            time_food = times[0].text
            time_food = time_food.replace("/", "-")
            Dict_for_a_recipe["post_time"] = time_food
            # 幾人份
            Dict_for_a_recipe["quantity"] = "1份"
            # 食材
            ingredients = soup_third.select('dl[class="recipe"] dd')
            list_of_ingredients = []
            for i in ingredients:
                x = i.text.split("\n")
                for ingredient in x:
                    d = {}
                    d["ingredient_names"] = ingredient
                    d["ingredient_units"] = "1"
                    list_of_ingredients.append(d)
            Dict_for_a_recipe["ingredients"] = list_of_ingredients
            # 步驟
            steps = soup_third.select('div[class="word"]')
            list_of_steps = [{"steps": n + 1, "methods": step.p.text} for n, step in enumerate(steps)]
            Dict_for_a_recipe["cooking_steps"] = list_of_steps

            # 如果是select('div[class="word"]' p) 代表多個div[class="word"]下層的所有p都要抓到
            # 但是我把p寫在回圈內step.p則只會抓到多個div[class="word"]下層的第一個p,剛好可以避開TIP都在第二個
            time.sleep(random.random())
            print(Dict_for_a_recipe)
            with open("%s/food_json_%s.txt"%(path2,no_article_thrd),"a+",encoding="utf-8") as f:
                json.dump(Dict_for_a_recipe,f)

        except IndexError as e:
            print(e)  # 頁配文的文章格式與平常的不同，篇幅較少，就不抓

def main():
    t0 = time.time()
    print("start")
    queue=mp.JoinableQueue()
    for i in range(6):
        worker_i=mp.Process(target=worker,args=(i+1,queue))
        worker_i.daemon=True
        worker_i.start()
        print(worker_i)
    producer(queue)
    queue.join()
    print(time.time() - t0, "seconds time")
if __name__ == "__main__":
    main()
