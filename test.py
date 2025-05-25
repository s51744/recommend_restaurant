import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json
import random
import datetime
import winsound

with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

root = tk.Tk()
root.title("餐廳選擇機")
root.geometry("600x700")  # 多一點高度放資訊

label_info = tk.Label(root, text="點擊按鈕抽一間餐廳", font=("微軟正黑體", 16))
label_info.pack(pady=10)

frame_img = tk.Frame(root, width=500, height=400, bg="#eee", relief=tk.SUNKEN)
frame_img.pack(pady=10)
frame_img.pack_propagate(False)

label_img = tk.Label(frame_img, text="圖片顯示區", bg="#eee")
label_img.pack(expand=True)

#新增標籤顯示營業狀態和卡路里
label_open = tk.Label(root, text="營業狀態：", font=("微軟正黑體", 14))
label_open.pack(pady=5)

label_calories = tk.Label(root, text="卡路里：", font=("微軟正黑體", 14))
label_calories.pack(pady=5)

def random_pick():
    winsound.MessageBeep()
    if not restaurants:
        messagebox.showinfo("提醒", "目前沒有餐廳資料")
        return
    chosen = random.choice(restaurants)
    
    info = f"餐廳：{chosen['name']}\n地址：{chosen['address']}"
    label_info.config(text=info)

    # 取得今天星期幾英文（跟 json 裡的 key 對應）
    today = datetime.datetime.today().strftime("%A")
    
    # 判斷是否營業
    hours = chosen.get('hours', {})
    open_status = hours.get(today, "不明")
    if open_status == "休息":
        open_text = "今天休息"
    elif open_status == "不明":
        open_text = "營業時間未知"
    else:
        open_text = f"今天營業時間：{open_status}"
    label_open.config(text="營業狀態：" + open_text)
    
    # 卡路里
    calories = chosen.get('calories', '未知')
    label_calories.config(text=f"卡路里：{calories} 大卡")
    
    # 圖片
    url = chosen.get('image_url', '')
    if url:
        try:
            response = requests.get(url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            max_size = (500, 400)
            img.thumbnail(max_size, Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            label_img.config(image=photo, text='')
            label_img.image = photo
        except Exception as e:
            label_img.config(image='', text="圖片載入失敗")
            label_img.image = None
    else:
        label_img.config(image='', text="沒有圖片網址")
        label_img.image = None

btn_pick = tk.Button(root, text="隨機抽餐廳", font=("微軟正黑體", 14), command=random_pick)
btn_pick.pack(pady=10)

root.mainloop()
