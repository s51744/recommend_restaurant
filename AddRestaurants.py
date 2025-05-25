import json

# 讀取現有餐廳資料
with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

print("請輸入新餐廳資料：")

#輸入餐廳名稱
name = input("名稱: ").strip()
#輸入地址
address = input("地址: ").strip()

#輸入營業時間，星期一到日
hours = {}
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for day in weekdays:
    h = input(f"{day} 營業時間（格式10:00-21:00 若休息請輸入 休息）: ").strip()
    hours[day] = h

image_url = input("圖片網址: ").strip()

#卡路里輸入，要轉成 int，失敗就設為 -1
calories_str = input("卡路里 (整數): ").strip()
try:
    calories = int(calories_str)
except:
    calories = -1

#建立新餐廳d
new_restaurant = {
    "name": name,
    "address": address,
    "hours": hours,
    "image_url": image_url,
    "calories": calories
}

# 檢查是否有欄位缺少或錯誤
required_fields = ["name", "address", "hours", "image_url", "calories"]
missing_fields = []
for field in required_fields:
    val = new_restaurant[field]
    if val == "" or val is None:
        missing_fields.append(field)
if calories == -1:
    missing_fields.append("calories (非整數)")

if missing_fields:
    print(f"❌ 無法新增，缺少或格式錯誤欄位：{', '.join(missing_fields)}")
else:
    # 檢查是否名稱重複
    if any(r["name"] == name for r in restaurants):
        print("⚠️ 此餐廳名稱已存在，無法重複新增。")
    else:
        restaurants.append(new_restaurant)
        with open('restaurants.json', 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, ensure_ascii=False, indent=2)
        print("✅ 餐廳新增成功！")
