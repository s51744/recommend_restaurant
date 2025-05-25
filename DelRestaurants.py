import json

def delete_restaurant_by_name(filename='restaurants.json'):
    #讀取資料
    with open(filename, 'r', encoding='utf-8') as f:
        restaurants = json.load(f)

    name_to_delete = input("請輸入要刪除的餐廳名稱：").strip()

    #用來判斷是否刪除成功
    found = False

    #篩選不等於要刪除名稱的餐廳，回傳新清單
    new_restaurants = []
    for r in restaurants:
        if r["name"] == name_to_delete:
            found = True
        else:
            new_restaurants.append(r)

    if found:
        #寫回檔案
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(new_restaurants, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功刪除餐廳：{name_to_delete}")
    else:
        print(f"⚠️ 找不到名稱為「{name_to_delete}」的餐廳。")

if __name__ == "__main__":
    delete_restaurant_by_name()
