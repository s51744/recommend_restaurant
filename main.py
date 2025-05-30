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
root.title("餐廳選擇機")
root.geometry("650x700")  # 降低高度從950到700
root.configure(bg=bg_color)

# 標題
title_label = tk.Label(root, text="📷 餐廳選擇機", bg=bg_color, font=("微軟正黑體", 16, "bold"))  # 縮小字體
title_label.pack(pady=10)  # 減少間距

# 副標題
subtitle_label = tk.Label(root, text="點擊按鈕，為您的午餐尋找靈感！", bg=bg_color, font=("微軟正黑體", 11))
subtitle_label.pack(pady=(0, 15))  # 減少間距

# 提示文字
prompt_label = tk.Label(root, text="點擊按鈕開始選擇！", bg=bg_color, font=("微軟正黑體", 12), fg="#ff8c00")
prompt_label.pack(pady=8)  # 減少間距

# 圖片顯示區域 - 縮小高度
frame_img = tk.Frame(root, width=500, height=200, bg="white", relief=tk.SUNKEN, bd=1)  # 縮小尺寸
frame_img.pack(pady=10)  # 減少間距
frame_img.pack_propagate(False)

label_img = tk.Label(frame_img, text="（圖片顯示區）", bg="white", font=("微軟正黑體", 11), fg="gray")
label_img.pack(expand=True, fill=tk.BOTH)

# 餐廳資訊顯示區
info_frame = tk.Frame(root, bg=bg_color)
info_frame.pack(pady=10)  # 減少間距

label_open = tk.Label(info_frame, text="營業狀態：　未知", bg=bg_color, font=("微軟正黑體", 11), anchor="w")
label_open.pack(anchor="w", padx=50)

label_price = tk.Label(info_frame, text="平均價格：　未知", bg=bg_color, font=("微軟正黑體", 11), anchor="w")
label_price.pack(anchor="w", padx=50, pady=2)  # 減少間距

label_calories = tk.Label(info_frame, text="卡路里：　未知", bg=bg_color, font=("微軟正黑體", 11), anchor="w")
label_calories.pack(anchor="w", padx=50)

# 按鈕區域
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=15)  # 減少間距

# 第一排按鈕 - 縮小按鈕高度
first_row = tk.Frame(button_frame, bg=bg_color)
first_row.pack(pady=3)

def toggle_open_today():
    picker.set_filter_open_today(not picker.filter_open_today)
    btn_filter.config(text=f"只抽今日有營業 ({'ON' if picker.filter_open_today else 'OFF'})")

btn_filter = tk.Button(first_row, text="只抽今日有營業 (OFF)", 
                      bg="#ffb347", activebackground="#ff7f50", font=("微軟正黑體", 11), 
                      relief="flat", width=15, height=1, command=toggle_open_today)  # 縮小按鈕
btn_filter.pack(side=tk.LEFT, padx=5)

def toggle_mode():
    picker.set_quick_mode(not picker.quick_mode)
    btn_toggle.config(text=f"🎯　模式: {'慢速模式' if picker.quick_mode else '慢速模式'}")

btn_toggle = tk.Button(first_row, text="🎯　模式: 慢速模式", 
                      bg="#ffb347", activebackground="#ff7f50", font=("微軟正黑體", 11), 
                      relief="flat", width=15, height=1, command=toggle_mode)  # 縮小按鈕
btn_toggle.pack(side=tk.LEFT, padx=5)

# 第二排按鈕
second_row = tk.Frame(button_frame, bg=bg_color)
second_row.pack(pady=5)

btn_pick = tk.Button(second_row, text="🎲 隨機抽餐廳", font=("微軟正黑體", 11), 
                    bg="#ffb347", activebackground="#ffa033", relief="flat", 
                    width=32, height=1)  # 縮小按鈕
btn_pick.pack()

# 輸入區域
input_frame = tk.Frame(root, bg=bg_color)
input_frame.pack(pady=15)  # 減少間距

input_label = tk.Label(input_frame, text="輸入您的喜好（例如：便宜的拉麵、牛肉麵）：", 
                      bg=bg_color, font=("微軟正黑體", 11))
input_label.pack()

entry_preference = tk.Entry(input_frame, font=("微軟正黑體", 11), width=45, relief="solid", bd=1)  # 縮小輸入框
entry_preference.pack(pady=8)  # 減少間距
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
    font=("微軟正黑體", 12, "bold"),
    bg="#90ee90",
    activebackground="#77dd77",
    relief="flat",
    command=get_recommendation,
    width=22,
    height=2
)
btn_ai.pack(pady=10)  # 減少間距

# 初始化picker
picker = RandomPicker(restaurants, prompt_label, label_img, label_open, label_price, label_calories, btn_pick, root)
btn_pick.config(command=picker.start)

# 讓視窗可以調整大小，並設定最小尺寸
root.resizable(True, True)
root.minsize(600, 650)

root.mainloop()