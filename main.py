import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker
from agent_utils import get_ai_recommendation

# 載入餐廳資料
with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# --- 顏色與樣式設定 ---
bg_color = "#1e1e2f"
fg_color = "white"
btn_color = "#3a3a5a"
accent_color = "#00ffc3"

root = tk.Tk()
root.title("餐廳選擇機")
root.geometry("980x600")
root.configure(bg=bg_color)
root.resizable(True, True)

# --- 標題 ---
title_label = tk.Label(root, text="🍜 餐廳選擇機", bg=bg_color, fg=accent_color,
                       font=("微軟正黑體", 20, "bold"))
title_label.pack(pady=10)

# --- 主框架 ---
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

# --- 左側圖片區 ---
left_frame = tk.Frame(main_frame, bg=bg_color, bd=2, relief=tk.RIDGE)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# 固定圖片區尺寸
frame_img = tk.Frame(left_frame, width=500, height=350, bg="black", bd=2)
frame_img.pack()
frame_img.pack_propagate(False)

label_img = tk.Label(frame_img, text="（圖片區）", bg="black", fg="gray",
                     font=("微軟正黑體", 12), anchor="center")
label_img.pack(fill=tk.BOTH, expand=True)

# --- 中間動畫/資訊區 ---
center_frame = tk.Frame(main_frame, bg=bg_color)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

prompt_label = tk.Label(center_frame, text="🎰 S P I N 🎰", fg=accent_color, bg=bg_color,
                         font=("Courier", 32, "bold"))
prompt_label.pack(pady=10)

label_info = tk.Label(center_frame, text="請點擊按鈕開始抽選...", bg=bg_color, fg=fg_color,
                      font=("微軟正黑體", 12), justify="left", wraplength=380, anchor="w")
label_info.pack(pady=5, fill=tk.X)

# --- 按鈕區 ---
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=15)

def toggle_open_today():
    picker.set_filter_open_today(not picker.filter_open_today)
    btn_filter.config(text=f"只抽今日有營業 ({'ON' if picker.filter_open_today else 'OFF'})")

btn_filter = tk.Button(btn_frame, text="只抽今日有營業 (OFF)", command=toggle_open_today,
                       bg=btn_color, fg=fg_color, activebackground=accent_color,
                       font=("微軟正黑體", 11), width=22, relief="flat")
btn_filter.pack(side=tk.LEFT, padx=10)

def toggle_mode():
    picker.set_quick_mode(not picker.quick_mode)
    btn_toggle.config(text=f"🎯 模式: {'快速模式' if picker.quick_mode else '慢速模式'}")

btn_toggle = tk.Button(btn_frame, text="🎯 模式: 慢速模式", command=toggle_mode,
                       bg=btn_color, fg=fg_color, activebackground=accent_color,
                       font=("微軟正黑體", 11), width=22, relief="flat")
btn_toggle.pack(side=tk.LEFT, padx=10)

btn_pick = tk.Button(btn_frame, text="🎲 隨機抽餐廳", font=("微軟正黑體", 11, "bold"),
                     command=None, bg=accent_color, fg="black", relief="flat", width=22)
btn_pick.pack(side=tk.LEFT, padx=10)

# --- AI 區 ---
def get_recommendation():
    preference = entry_preference.get()
    if not preference:
        messagebox.showwarning("輸入錯誤", "請輸入你的午餐偏好")
        return
    result = get_ai_recommendation(preference, restaurants)
    messagebox.showinfo("AI 推薦結果", result)

entry_preference = tk.Entry(root, font=("微軟正黑體", 11), width=40)
entry_preference.pack(pady=5)
entry_preference.insert(0, "")

btn_ai = tk.Button(root, text="🤖 AI 推薦午餐", font=("微軟正黑體", 12, "bold"),
                   command=get_recommendation, bg="#00ffaa", fg="black",
                   relief="flat", width=22)
btn_ai.pack(pady=10)

# 初始化 Picker
picker = RandomPicker(restaurants, label_info, label_img, btn_pick, root)

btn_pick.config(command=picker.start)

root.mainloop()
