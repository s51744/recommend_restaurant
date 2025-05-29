# main.py
import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker
from agent_utils import get_ai_recommendation

# 載入餐廳資料
with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

bg_color = "#f5f5f5"
root = tk.Tk()
root.title("AI 餐廳選擇機")
root.geometry("650x950")
root.configure(bg=bg_color)

# 標題
title_label = tk.Label(root, text="📷 AI 餐廳選擇機", bg=bg_color, font=("微軟正黑體", 18, "bold"))
title_label.pack(pady=15)

# 副標題
subtitle_label = tk.Label(root, text="點擊按鈕，為您的午餐尋找靈感！", bg=bg_color, font=("微軟正黑體", 12))
subtitle_label.pack(pady=(0, 20))

# 提示文字
prompt_label = tk.Label(root, text="點擊按鈕開始選擇！", bg=bg_color, font=("微軟正黑體", 14), fg="#ff8c00")
prompt_label.pack(pady=10)

# 圖片顯示區域
frame_img = tk.Frame(root, width=550, height=250, bg="white", relief=tk.SUNKEN, bd=1)
frame_img.pack(pady=15)
frame_img.pack_propagate(False)

label_img = tk.Label(frame_img, text="（圖片顯示區）", bg="white", font=("微軟正黑體", 12), fg="gray")
label_img.pack(expand=True, fill=tk.BOTH)

# 餐廳資訊顯示區
info_frame = tk.Frame(root, bg=bg_color)
info_frame.pack(pady=15)

label_open = tk.Label(info_frame, text="營業狀態：　未知", bg=bg_color, font=("微軟正黑體", 12), anchor="w")
label_open.pack(anchor="w", padx=50)

label_price = tk.Label(info_frame, text="平均價格：　未知", bg=bg_color, font=("微軟正黑體", 12), anchor="w")
label_price.pack(anchor="w", padx=50, pady=3)

label_calories = tk.Label(info_frame, text="距離公司：　未知", bg=bg_color, font=("微軟正黑體", 12), anchor="w")
label_calories.pack(anchor="w", padx=50)

# 按鈕區域
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=20)

# 第一排按鈕
first_row = tk.Frame(button_frame, bg=bg_color)
first_row.pack(pady=5)

btn_pick = tk.Button(first_row, text="🎲 隨機抽餐廳", font=("微軟正黑體", 12), 
                    bg="#ffb347", activebackground="#ffa033", relief="flat", 
                    width=16, height=2)
btn_pick.pack(side=tk.LEFT, padx=5)

def toggle_mode():
    picker.set_quick_mode(not picker.quick_mode)
    btn_toggle.config(text=f"🎯　模式: {'慢速模式' if picker.quick_mode else '慢速模式'}")

btn_toggle = tk.Button(first_row, text="🎯　模式: 慢速模式", 
                      bg="#ffb347", activebackground="#ff7f50", font=("微軟正黑體", 12), 
                      relief="flat", width=16, height=2, command=toggle_mode)
btn_toggle.pack(side=tk.LEFT, padx=5)

# 第二排按鈕
second_row = tk.Frame(button_frame, bg=bg_color)
second_row.pack(pady=10)

def toggle_open_today():
    picker.set_filter_open_today(not picker.filter_open_today)
    btn_filter.config(text=f"只抽今日有營業 ({'ON' if picker.filter_open_today else 'OFF'})")

btn_filter = tk.Button(second_row, text="只抽今日有營業 (OFF)", 
                      bg="#ffb347", activebackground="#ff7f50", font=("微軟正黑體", 12), 
                      relief="flat", width=34, height=2, command=toggle_open_today)
btn_filter.pack()

# 輸入區域
input_frame = tk.Frame(root, bg=bg_color)
input_frame.pack(pady=20)

input_label = tk.Label(input_frame, text="輸入您的喜好（例如：便宜的拉麵、牛肉麵）：", 
                      bg=bg_color, font=("微軟正黑體", 12))
input_label.pack()

entry_preference = tk.Entry(input_frame, font=("微軟正黑體", 12), width=50, relief="solid", bd=1)
entry_preference.pack(pady=10)
entry_preference.insert(0, "我想吃便宜的拉麵")

# AI推薦按鈕
def get_recommendation():
    preference = entry_preference.get()
    if not preference:
        messagebox.showwarning("輸入錯誤", "請輸入你的午餐偏好")
        return
    result = get_ai_recommendation(preference, restaurants)
    messagebox.showinfo("AI 推薦結果", result)

btn_ai = tk.Button(
    root,
    text="🍱 AI 智能推薦午餐",
    font=("微軟正黑體", 14, "bold"),
    bg="#90ee90",
    activebackground="#77dd77",
    relief="flat",
    command=get_recommendation,
    width=25,
    height=2
)
btn_ai.pack(pady=15)

# 初始化picker
picker = RandomPicker(restaurants, prompt_label, label_img, label_open, label_price, label_calories, btn_pick, root)
btn_pick.config(command=picker.start)

root.mainloop()