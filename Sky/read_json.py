import json,os
path2=r'./collction'
with open("%s/food_json_1902.txt"%(path2), "r", encoding="utf-8") as f:
    d=f.read()
    d = json.loads(d)
    print(d)