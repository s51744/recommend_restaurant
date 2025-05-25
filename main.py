import json
import random
import datetime

#載入餐廳資料
with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)
    
#取得今天是星期幾
today = datetime.datetime.today().strftime('%A')  # Monday, Tuesday...

#隨機抽一間
chosen = random.choice(restaurants)

print(f"今天吃：{chosen['name']}")
print(f"地址：{chosen['address']}")
#顯示今天營業時間
open_hours_today = chosen['hours'].get(today, "不明")
print(f"今天 ({today}) 營業時間：{open_hours_today}")
