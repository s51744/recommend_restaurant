import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker
from agent_utils import get_ai_recommendation
from restaurant_manager import open_manager_window
from PIL import Image, ImageTk
import requests
from io import BytesIO

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
root.geometry("980x690")
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

frame_img = tk.Frame(left_frame, width=500, height=410, bg="black", bd=2)
frame_img.pack()
frame_img.pack_propagate(False)

response = requests.get("https://image.cache.storm.mg/styles/smg-800x533-fp/s3/media/image/2017/03/28/20170328-031700_U7298_M262448_8adf.jpg?itok=7-Rokk_a")
img_data = response.content
img = Image.open(BytesIO(img_data))
img.thumbnail((500, 400), Image.LANCZOS)
photo = ImageTk.PhotoImage(img)

label_img = tk.Label(frame_img, image=photo, bg="black")
label_img.image = photo
label_img.pack(fill=tk.BOTH, expand=True)

# --- 中間動畫/資訊區 ---
center_frame = tk.Frame(main_frame, bg=bg_color)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

prompt_label = tk.Label(center_frame, text="🎰 S P I N 🎰", fg=accent_color, bg=bg_color,
                         font=("Courier", 32, "bold"))
prompt_label.pack(pady=10)

label_info = tk.Label(center_frame,
    text=(
        "請點擊下方按鈕開始抽選...\n\n"
        "📜 規則小提醒：\n"
        "1. 可以選擇是否只抽今日營業\n"
        "2. 可設定卡路里與價格範圍,若未輸入就是0與∞\n"
        "3. 有快速／慢速模式可做切換\n\n"
        "讓命運決定你的午餐，也許下一餐就是命中注定！"
        "\n\n\n\n\n\n\n\n還不趕緊點擊按鈕抽選...等的我都餓了"
    ),
    bg=bg_color, fg=fg_color, font=("微軟正黑體", 12),
    justify="left", wraplength=380, anchor="w")

label_info.pack(pady=5, fill=tk.X)

# --- 篩選欄位（卡路里 / 價格） ---
filter_frame = tk.Frame(root, bg=bg_color)
filter_frame.pack(pady=(0, 10))

def create_range_input(label_text, min_var, max_var):
    tk.Label(filter_frame, text=label_text, bg=bg_color, fg=fg_color,
             font=("微軟正黑體", 12)).pack(side=tk.LEFT, padx=(0, 4))
    min_var.pack(side=tk.LEFT)
    tk.Label(filter_frame, text="～", bg=bg_color, fg=fg_color).pack(side=tk.LEFT)
    max_var.pack(side=tk.LEFT, padx=(0, 20))

entry_cal_min = tk.Entry(filter_frame, width=6)
entry_cal_max = tk.Entry(filter_frame, width=6)
create_range_input("卡路里", entry_cal_min, entry_cal_max)

entry_price_min = tk.Entry(filter_frame, width=6)
entry_price_max = tk.Entry(filter_frame, width=6)
create_range_input("價格", entry_price_min, entry_price_max)
# --- 按鈕區 ---
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=15)

def toggle_open_today():
    picker.set_filter_open_today(not picker.filter_open_today)
    btn_filter.config(text=f"只抽今日有營業 ({'ON' if picker.filter_open_today else 'OFF'})")

btn_filter = tk.Button(btn_frame, text="只抽今日有營業 (OFF)", command=toggle_open_today,
                       bg=btn_color, fg=fg_color, activebackground=accent_color,
                       font=("微軟正黑體", 14, "bold"), width=24, padx=14, pady=8)
btn_filter.pack(side=tk.LEFT, padx=10)

def toggle_mode():
    picker.set_quick_mode(not picker.quick_mode)
    btn_toggle.config(text=f"🎯 模式: {'快速模式' if picker.quick_mode else '慢速模式'}")

btn_toggle = tk.Button(btn_frame, text="🎯 模式: 慢速模式", command=toggle_mode,
                       bg=btn_color, fg=fg_color, activebackground=accent_color,
                       font=("微軟正黑體", 14, "bold"), width=24, padx=14, pady=8)
btn_toggle.pack(side=tk.LEFT, padx=10)

btn_pick = tk.Button(btn_frame, text="🎲 隨機抽餐廳", font=("微軟正黑體", 14, "bold"),
                     width=24, padx=14, pady=8, command=None,
                     bg=accent_color, fg="black", relief="flat")
btn_pick.pack(side=tk.LEFT, padx=10)

btn_manage = tk.Button(root, text="📂 管理餐廳資料", command=open_manager_window,
                       bg="#3a3a5a", fg="white", font=("微軟正黑體", 11), relief="flat")
btn_manage.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)



# --- AI 區 ---
def get_recommendation():
    preference = entry_preference.get()
    if not preference:
        messagebox.showwarning("輸入錯誤", "請輸入你的午餐偏好")
        return
    result = get_ai_recommendation(preference, restaurants)
    messagebox.showinfo("AI 推薦結果", result)

ai_input_frame = tk.Frame(root, bg=bg_color)
ai_input_frame.pack(pady=10)

entry_preference = tk.Entry(ai_input_frame, font=("微軟正黑體", 11), width=40)
entry_preference.pack(side=tk.LEFT, padx=(0, 10))
entry_preference.insert(0, "")

btn_ai = tk.Button(ai_input_frame, text="🤖 AI 推薦午餐", font=("微軟正黑體", 11, "bold"),
                   command=get_recommendation, bg="#00ffaa", fg="black",
                   relief="flat", width=18)
btn_ai.pack(side=tk.LEFT, padx=(10, 0))

# --- 初始化 Picker ---
picker = RandomPicker(restaurants, label_info, label_img, btn_pick, root)

def safe_int(entry, default):
    val = entry.get().strip()
    return int(val) if val.isdigit() else default

def start_with_filter():
    try:
        cal_min = safe_int(entry_cal_min, 0)
        cal_max = safe_int(entry_cal_max, 99999)
        price_min = safe_int(entry_price_min, 0)
        price_max = safe_int(entry_price_max, 99999)
        picker.set_calorie_range(cal_min, cal_max)
        picker.set_price_range(price_min, price_max)
        picker.start()
    except Exception as e:
        messagebox.showerror("錯誤", f"請確認欄位內容為數字\\n錯誤訊息：{str(e)}")

btn_pick.config(command=start_with_filter)

root.mainloop()
