import pandas as pd
import MySQLdb,random

#user_id
n=1
#幾個推薦食譜
m=10


def sql_query(query):
    cursor.execute(query)
    datarows=cursor.fetchall()
    return datarows

def update_to_sql(sql_update):
    cursor.execute(sql_update)

#第0步:更改成可寫入
def step_0():
    change_safe_update = 'SET SQL_SAFE_UPDATES=0;'
    update_to_sql(change_safe_update)

#疊代相加
def plus(data_tag,n,m):
    if m==(n+1):
        return data_tag[n]
    else:
        for i in range(n, m - 1):
            data_tag[i + 1] = data_tag[i] + data_tag[i + 1]
            tmp = data_tag[i + 1]
        return tmp
def tag_compute(data_tag):
    point_list=[1,4,7,9,10,12,14,18,19,20,23,24,25,27]
    list_text_cluster_score=[]
    list_nutrition_cluster_score=[]
    for n,i in enumerate(point_list):
        #第一建模
        if i <9 :
            tmp=plus(data_tag, point_list[n], point_list[n + 1])
            list_text_cluster_score.append(tmp)
        #第二建模
        elif i >=9 and n<len(point_list)-1:
            tmp=plus(data_tag, point_list[n], point_list[n + 1])
            list_nutrition_cluster_score.append(tmp)
    text_cluster=list_text_cluster_score.index(max(list_text_cluster_score))+1
    nutrition_cluster=list_nutrition_cluster_score.index(max(list_nutrition_cluster_score))+1
    return text_cluster,nutrition_cluster

def step_1(n):
    query_1="select * from users_tags where user={}".format(n)
    datarows=sql_query(query_1)
    data_tag=list(list(datarows)[0])
    text_cluster,nutrition_cluster=tag_compute(data_tag)
    query_2 = "select * from km_10_clusters where cluster={} and text_cluster={}".format(nutrition_cluster,text_cluster)
    cluster_intersection=sql_query(query_2)
    return cluster_intersection

def top_m(cluster_intersection,m):
    top10_tuple=random.sample(list(cluster_intersection),k=m)
    top10_df=pd.DataFrame(list(top10_tuple))
    print(top10_df)
    return list(top10_df.iloc[:,0])

def main(n,m):
    step_0()
    cluster_intersection=step_1(n)
    id_list=top_m(cluster_intersection,m)

    print(id_list)

if __name__=="__main__":
    db = MySQLdb.connect(host="114.44.75.12", user="user", passwd="user", db="iii_project", port=3306, charset="utf8")
    cursor = db.cursor()
    db.autocommit(True)
    main(n,m)
    db.close()