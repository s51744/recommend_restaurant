import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker

with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

root = tk.Tk()
root.title("餐廳選擇機")
root.geometry("600x650")

label_info = tk.Label(root, text="點擊按鈕抽一間餐廳", font=("微軟正黑體", 16))
label_info.pack(pady=10)

frame_img = tk.Frame(root, width=500, height=400, bg="#eee", relief=tk.SUNKEN)
frame_img.pack(pady=10)
frame_img.pack_propagate(False)

label_img = tk.Label(frame_img, text="圖片顯示區", bg="#eee")
label_img.pack(expand=True)

label_open = tk.Label(root, text="營業狀態：", font=("微軟正黑體", 14))
label_open.pack(pady=5)

label_calories = tk.Label(root, text="卡路里：", font=("微軟正黑體", 14))
label_calories.pack(pady=5)

btn_pick = tk.Button(root, text="隨機抽餐廳", font=("微軟正黑體", 14))
btn_pick.pack(pady=10)

picker = RandomPicker(restaurants, label_info, label_img, label_open, label_calories, btn_pick, root)
btn_pick.config(command=picker.start)

root.mainloop()
