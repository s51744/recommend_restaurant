import tkinter as tk
from tkinter import messagebox
import json
from random_anim import RandomPicker

with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)
    
bg_color = "#fdf6e3"
root = tk.Tk()
root.title("餐廳選擇機")
root.geometry("600x900")

label_info = tk.Label(root, text="點擊按鈕抽一間餐廳",  bg=bg_color, font=("微軟正黑體", 16))
label_info.pack(pady=10)

root.configure(bg=bg_color)  #奶茶色背景
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

btn_pick = tk.Button(
    root,
    text="🎲 隨機抽餐廳",
    font=("微軟正黑體", 14),
    bg="#ffb347",
    #fg="white",
    activebackground="#ffa033",
    relief="flat",
    padx=20,
    pady=10
)
btn_pick.pack(pady=10)

picker = RandomPicker(restaurants, label_info, label_img, label_open, label_price, label_calories, btn_pick, root)
btn_pick.config(command=picker.start)
#只抽本日有營業的店
def toggle_open_today():
    picker.set_filter_open_today(not picker.filter_open_today)
    if picker.filter_open_today:
        btn_filter.config(text="只抽今日有營業 (ON)")
    else:
        btn_filter.config(text="只抽今日有營業 (OFF)")
btn_filter = tk.Button(root, text="只抽今日有營業 (OFF)",  bg="#ffb347", activebackground = "#ff7f50", font=("微軟正黑體", 14),relief="flat", command=toggle_open_today)
btn_filter.pack(pady=10)
        
#快速模式切換按鈕
def toggle_mode():
    picker.set_quick_mode(not picker.quick_mode)
    mode_text = "快速模式" if picker.quick_mode else "慢速模式"
    btn_toggle.config(text=f"切換模式 (目前：{mode_text})")

btn_toggle = tk.Button(root, text="切換模式 (目前：慢速模式)",  bg="#ffb347", activebackground = "#ff7f50", font=("微軟正黑體", 14),relief="flat", command=toggle_mode)
btn_toggle.pack(pady=10)

root.mainloop()
