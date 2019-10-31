import jieba
import os

source_path = r'E:\food' #讀取資料夾位子
file_list = os.listdir(source_path)
print(file_list)



article_str = ''
for article in file_list:
    with open(source_path + '/' + article, 'r', encoding='UTF-8') as f:
        article_str += f.read()
print(article_str)



new_str = article_str.replace('\n',' ')
#不需要換行符號用空格(' ')去取代他
s = jieba.cut(new_str)
'|'.join(s)#用 '|'.join(s)把每一個詞分開

new_str = article_str.replace('\n',' ')
s = jieba.cut(new_str)
#用字典計算每個字在做排序
word_count = {} #2.宣告空字典
for w in '|'.join(s).split('|'): #1.用split做分割,放入迴圈
    if w in word_count: #如果這字在字典裡面
        word_count[w] += 1 #就讓這個字+1
    else: #如果不再字典裡面
        word_count[w] = 1 #就讓這個字=1
print(word_count)

#先變成list
word_count_list = []#設定一個空list
for wc in word_count:
    word_count_list.append((wc, word_count[wc]))#在word_count新增(key,valu)
print(word_count_list)

#做排序 使用lamdba函數讓第幾個值做排序
word_count_list.sort(key = lambda x:x[1], reverse = True)
#x:x冒號前面是輸入什麼
#x:x[1]冒號後面是輸出什麼,輸出x第一個東西 EX:('[0]','[1]')
print(word_count_list)


