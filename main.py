import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker
from agent_utils import get_ai_recommendation
from restaurant_manager import open_manager_window
from PIL import Image, ImageTk
import requests
from io import BytesIO
import pygame
import threading
import webbrowser
from datetime import datetime

# 初始化音效
pygame.mixer.init()
pygame.mixer.music.load("sounds/bg.wav")
pygame.mixer.music.play(-1)  # -1 表示無限循環

sound_enabled = True
music_enabled = True

def open_map_for_restaurant(name, address=""):
    if name:
        query = f"{name} {address}".replace(" ", "+")
        url = f"https://www.google.com/maps/search/?api=1&query={query}"
        webbrowser.open(url)
    else:
        messagebox.showwarning("錯誤", "請先抽選餐廳")

# 音效播放函式
def play_sound(sound_path):
    def _play():
        try:
            pygame.mixer.Sound(sound_path).play()
        except Exception as e:
            print(f"音效播放失敗: {e}")
    threading.Thread(target=_play, daemon=True).start()

# 音樂控制函式
def toggle_music():
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        pygame.mixer.music.play(-1)
        btn_music.config(text="🎵")
    else:
        pygame.mixer.music.stop()
        btn_music.config(text="❌")

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
root.geometry("980x695")
root.configure(bg=bg_color)
root.resizable(False, False)  #禁止水平與垂直調整視窗大小

# 音效開關按鈕（僅控制背景音樂）
btn_music = tk.Button(root, text="🎵", command=toggle_music,
                      bg=bg_color, fg="white", font=("微軟正黑體", 12), relief="flat")
btn_music.place(x=10, y=10)

# --- 時間顯示在右上角 ---
def update_time():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=now)
    root.after(1000, update_time)

time_label = tk.Label(root, font=("微軟正黑體", 10), fg="#cccccc", bg=bg_color)
time_label.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

update_time()

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
    "1. 左上角可以把好聽的背景音樂關閉\n"
    "2. 可選擇是否只抽出今日營業的餐廳\n"
    "3. 右上角有提醒目前時間，別撲空了\n"
    "4. 可自訂卡路里與價格範圍，留空則預設為 0～∞\n"
    "5. 可切換『快速模式』與『慢速模式』\n"
    "6. 點擊左下角📂管理你的專屬餐廳清單\n"
    "7. 點擊下方🤖輸入偏好，讓AI幫你推薦\n"
    "8. 抽出後可點右下角📍一鍵開啟Google地圖查詢位置\n\n"
    "讓命運決定你的午餐，也許下一餐就是命中決定！"
    "\n\n\n還不趕緊點擊按鈕抽選...等的我都餓了"
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
    
def set_entry_hint(entry, hint_text):
    def on_focus_in(event):
        if entry.get() == hint_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, hint_text)
            entry.config(fg="gray")

    entry.insert(0, hint_text)
    entry.config(fg="gray")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    
entry_cal_min = tk.Entry(filter_frame, width=6)
entry_cal_max = tk.Entry(filter_frame, width=6)
set_entry_hint(entry_cal_min, "0")
set_entry_hint(entry_cal_max, "∞")
create_range_input("卡路里", entry_cal_min, entry_cal_max)

entry_price_min = tk.Entry(filter_frame, width=6)
entry_price_max = tk.Entry(filter_frame, width=6)
set_entry_hint(entry_price_min, "0")
set_entry_hint(entry_price_max, "∞")
create_range_input("價格", entry_price_min, entry_price_max)

# --- 初始化 Picker ---
picker = RandomPicker(restaurants, label_info, label_img, btn_pick=None, root=root)
selected_restaurant_name = None

def safe_int(entry, default):
    val = entry.get().strip()
    return int(val) if val.isdigit() else default

def toggle_open_today_with_sound():
    new_state = not picker.filter_open_today
    picker.set_filter_open_today(new_state)
    btn_filter.config(text=f"只抽今日有營業 ({'ON' if new_state else 'OFF'})")
    play_sound("sounds/open.wav" if new_state else "sounds/close.wav")

def toggle_mode_with_sound():
    new_state = not picker.quick_mode
    picker.set_quick_mode(new_state)
    btn_toggle.config(text=f"🎯 模式: {'快速模式' if new_state else '慢速模式'}")
    play_sound("sounds/open.wav" if new_state else "sounds/close.wav")

def start_with_filter():
    try:
        set_buttons_state("disabled")  # 🔒 全部按鈕關閉
        cal_min = safe_int(entry_cal_min, 0)
        cal_max = safe_int(entry_cal_max, 99999)
        price_min = safe_int(entry_price_min, 0)
        price_max = safe_int(entry_price_max, 99999)
        picker.set_calorie_range(cal_min, cal_max)
        picker.set_price_range(price_min, price_max)

        def after_spin():
            global selected_restaurant_name
            selected_restaurant_name = picker.last_picked_name
            btn_map.config(state=tk.NORMAL)
            set_buttons_state("normal")  # 🔓 恢復可點擊狀態

        picker.start(after_spin_callback=after_spin)

    except Exception as e:
        set_buttons_state("normal")  # 錯誤時也要恢復
        messagebox.showerror("錯誤", f"請確認欄位內容為數字\n錯誤訊息：{str(e)}")


def start_with_filter_with_sound():
    play_sound("sounds/button.mp3")
    start_with_filter()

def open_manager_window_with_sound():
    play_sound("sounds/box.wav")
    open_manager_window()

def get_recommendation():
    preference = entry_preference.get()
    if not preference:
        messagebox.showwarning("輸入錯誤", "請輸入你的午餐偏好")
        return
    result = get_ai_recommendation(preference, restaurants)
    messagebox.showinfo("AI 推薦結果", result)

def get_recommendation_with_sound():
    play_sound("sounds/bot.wav")
    
    get_recommendation()
def open_map_with_sound():
    play_sound("sounds/bye.wav")
    open_map_for_restaurant(picker.last_picked_name, picker.last_picked_address)
    
# --- 按鈕區 ---
btn_frame = tk.Frame(root, bg=bg_color)
btn_frame.pack(pady=15)

style_common = {
    "font": ("微軟正黑體", 14, "bold"),
    "width": 24,
    "padx": 14,
    "pady": 8,
    "relief": "raised",
    "bd": 3,
    "cursor": "hand2"
}

btn_filter = tk.Button(btn_frame, text="只抽今日有營業 (OFF)", command=toggle_open_today_with_sound,
                       bg=btn_color, fg=fg_color, activebackground=accent_color, **style_common)
btn_filter.pack(side=tk.LEFT, padx=10)

btn_toggle = tk.Button(btn_frame, text="🎯 模式: 慢速模式", command=toggle_mode_with_sound,
                       bg=btn_color, fg=fg_color, activebackground=accent_color, **style_common)
btn_toggle.pack(side=tk.LEFT, padx=10)

btn_pick = tk.Button(btn_frame, text="🎲 隨機抽餐廳", command=start_with_filter_with_sound,
                     bg=accent_color, fg="black", activebackground="#33ffcc", **style_common)
btn_pick.pack(side=tk.LEFT, padx=10)

picker.btn_pick = btn_pick

btn_manage = tk.Button(root, text="📂 管理餐廳資料", command=open_manager_window_with_sound,
                       bg="#3a3a5a", fg="white", font=("微軟正黑體", 11), relief="raised", bd=2, cursor="hand2")
btn_manage.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

btn_map = tk.Button(root, text="📍 打開地圖", font=("微軟正黑體", 11, "bold"),
    command=open_map_with_sound,
    bg="#00cc99", fg="black", activebackground="#00ffaa",
    relief="raised", bd=3, cursor="hand2", state=tk.DISABLED)
btn_map.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

def set_buttons_state(state):
    btn_filter.config(state=state)
    btn_toggle.config(state=state)
    btn_pick.config(state=state)
    btn_manage.config(state=state)
    btn_ai.config(state=state)
    btn_map.config(state=state if picker.last_picked_name else tk.DISABLED)

# --- AI 區 ---

ai_input_frame = tk.Frame(root, bg=bg_color)
ai_input_frame.pack(pady=10)

entry_preference = tk.Entry(ai_input_frame, font=("微軟正黑體", 11), width=40)
entry_preference.pack(side=tk.LEFT, padx=(0, 10))
set_entry_hint(entry_preference, "請輸入你想吃的餐點…")
btn_ai = tk.Button(ai_input_frame, text="🤖 AI 推薦午餐", font=("微軟正黑體", 11, "bold"),
                   command=get_recommendation_with_sound, bg="#00ffaa", fg="black",
                   relief="raised", bd=3, cursor="hand2", width=18)
btn_ai.pack(side=tk.LEFT, padx=(10, 0))

root.mainloop()
