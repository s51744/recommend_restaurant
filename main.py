# main.py
import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker
from agent_utils import get_ai_recommendation

# 載入餐廳資料
with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

bg_color = "#fdf6e3"
root = tk.Tk()
root.title("AI 餐廳選擇機")
root.geometry("600x900")
root.configure(bg=bg_color)

label_info = tk.Label(root, text="點擊按鈕抽一間餐廳",  bg=bg_color, font=("微軟正黑體", 16))
label_info.pack(pady=10)

frame_img = tk.Frame(root, width=500, height=400, bg=bg_color, relief=tk.SUNKEN)
frame_img.pack(pady=10)
frame_img.pack_propagate(False)

label_img = tk.Label(frame_img, text="圖片顯示區", bg="#eee")
label_img.pack(expand=True)

label_open = tk.Label(root, text="營業狀態：",  bg=bg_color, font=("微軟正黑體", 14))
label_open.pack(pady=5)

label_price = tk.Label(root, text="平均價格：", bg=bg_color, font=("微軟正黑體", 14))
label_price.pack(pady=5)

label_calories = tk.Label(root, text="卡路里：", bg=bg_color,  font=("微軟正黑體", 14))
label_calories.pack(pady=5)

btn_pick = tk.Button(root, text="\U0001F3B2 隨機抽餐廳", font=("微軟正黑體", 14), bg="#ffb347", activebackground="#ffa033", relief="flat", padx=20, pady=10)
btn_pick.pack(pady=10)

picker = RandomPicker(restaurants, label_info, label_img, label_open, label_price, label_calories, btn_pick, root)
btn_pick.config(command=picker.start)

def toggle_open_today():
    picker.set_filter_open_today(not picker.filter_open_today)
    btn_filter.config(text=f"只抽今日有營業 ({'ON' if picker.filter_open_today else 'OFF'})")

btn_filter = tk.Button(root, text="只抽今日有營業 (OFF)",  bg="#ffb347", activebackground="#ff7f50", font=("微軟正黑體", 14), relief="flat", command=toggle_open_today)
btn_filter.pack(pady=10)

def toggle_mode():
    picker.set_quick_mode(not picker.quick_mode)
    btn_toggle.config(text=f"切換模式 (目前：{'快速模式' if picker.quick_mode else '慢速模式'})")

btn_toggle = tk.Button(root, text="切換模式 (目前：慢速模式)",  bg="#ffb347", activebackground="#ff7f50", font=("微軟正黑體", 14), relief="flat", command=toggle_mode)
btn_toggle.pack(pady=10)

# 使用者輸入偏好 + AI 推薦功能
entry_preference = tk.Entry(root, font=("微軟正黑體", 14), width=40)
entry_preference.pack(pady=10)
entry_preference.insert(0, "我想吃便宜的拉麵")

def get_recommendation():
    preference = entry_preference.get()
    if not preference:
        messagebox.showwarning("輸入錯誤", "請輸入你的午餐偏好")
        return
    result = get_ai_recommendation(preference, restaurants)
    messagebox.showinfo("AI 推薦結果", result)

btn_ai = tk.Button(
    root,
    text="🍱 使用 AI 推薦午餐",
    font=("微軟正黑體", 16),  # 放大字體
    bg="#90ee90",
    activebackground="#77dd77",
    relief="flat",
    command=get_recommendation,
    width=30,  # 設定按鈕寬度（單位是字元）
    height=2   # 設定按鈕高度（單位是行數）
)
btn_ai.pack(pady=10)

root.mainloop()
