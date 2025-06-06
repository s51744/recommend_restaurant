import tkinter as tk
from tkinter import Toplevel, Scrollbar, Canvas, messagebox
from PIL import Image, ImageTk
import json
import requests
from io import BytesIO

bg_color = "#1e1e2f"
fg_color = "white"
border_color = "#444"
card_bg = "#2a2a3d"
font_main = ("微軟正黑體", 13)

with open('restaurants.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

def open_manager_window():
    manager = Toplevel()
    manager.title("🍱 餐廳資料管理")
    manager.geometry("1000x700")
    manager.configure(bg=bg_color)

    close_btn = tk.Button(manager, text="✖", command=manager.destroy,
                          bg=bg_color, fg="gray", font=("微軟正黑體", 10), relief="flat")
    close_btn.pack(anchor="ne", padx=10, pady=5)

    canvas = Canvas(manager, bg=bg_color, highlightthickness=0)
    scrollbar = Scrollbar(manager, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=bg_color)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for r in restaurants:
        card = tk.Frame(scroll_frame, bg=card_bg, bd=1, relief="solid")
        card.pack(padx=20, pady=15, fill="x")

        image_url = r.get('image_url', '')
        img_label = tk.Label(card, bg=card_bg)
        img_label.pack(side="left", padx=10, pady=10)

        if image_url:
            try:
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                img_label.config(image=photo)
                img_label.image = photo
            except:
                img_label.config(text="❌ 圖片載入失敗", fg="gray")
        else:
            img_label.config(text="無圖", fg="gray")

        info = tk.Frame(card, bg=card_bg)
        info.pack(side="left", fill="x", expand=True, padx=10)

        tk.Label(info, text=f"【 餐廳 】 {r['name']}", fg=fg_color, bg=card_bg, font=("微軟正黑體", 14, "bold"), anchor="w").pack(anchor="w", pady=3)
        tk.Label(info, text=f"【 地址 】 {r['address']}", fg=fg_color, bg=card_bg, font=font_main, anchor="w").pack(anchor="w", pady=3)

        tk.Label(info, text="營業時間：", fg=fg_color, bg=card_bg, font=font_main, anchor="w").pack(anchor="w", pady=(3, 0))
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in weekdays:
            time = r['hours'].get(day, "不明")
            label = f"{day:<10} {time}"
            tk.Label(info, text=label, fg=fg_color, bg=card_bg, font=("微軟正黑體", 11), anchor="w", justify="left").pack(anchor="w")

        tk.Label(info, text=f"【 價格 】 NT${r.get('price', '?')}", fg=fg_color, bg=card_bg, font=font_main, anchor="w").pack(anchor="w", pady=3)

        btns = tk.Frame(info, bg=card_bg)
        btns.pack(anchor="e", pady=5)

        def make_delete_func(name):
            return lambda: delete_restaurant(name, manager)

        def make_edit_func(data):
            return lambda: open_edit_form(data, manager)

        tk.Button(btns, text="📝 編輯", command=make_edit_func(r),
                  bg="#2196f3", fg="white", font=("微軟正黑體", 10), relief="flat", padx=8).pack(side="left", padx=5)

        tk.Button(btns, text="🗑 刪除", command=make_delete_func(r['name']),
                  bg="#ff4d4d", fg="white", font=("微軟正黑體", 10), relief="flat", padx=8).pack(side="left", padx=5)

    bottom_btn_frame = tk.Frame(manager, bg=bg_color)
    bottom_btn_frame.pack(side="bottom", anchor="se", pady=15, padx=15)

    tk.Button(bottom_btn_frame, text="✚ 新增餐廳", command=lambda: open_edit_form(None, manager),
              bg="#4caf50", fg="white", font=("微軟正黑體", 12), relief="flat", padx=10, pady=5).pack(anchor="e")

def delete_restaurant(name, window):
    global restaurants
    confirm = messagebox.askyesno("確定刪除", f"你確定要刪除「{name}」嗎？")
    if not confirm:
        return
    restaurants = [r for r in restaurants if r['name'] != name]
    with open('restaurants.json', 'w', encoding='utf-8') as f:
        json.dump(restaurants, f, ensure_ascii=False, indent=2)
    messagebox.showinfo("刪除成功", f"已刪除「{name}")
    window.destroy()
    open_manager_window()

def open_edit_form(data, parent):
    form = Toplevel(parent)
    form.title("編輯餐廳" if data else "新增餐廳")
    form.geometry("500x680")
    form.configure(bg=bg_color)

    def field(label, default=""):
        tk.Label(form, text=label, fg=fg_color, bg=bg_color, font=font_main).pack(pady=(10, 2), anchor="w", padx=20)
        entry = tk.Entry(form, font=font_main, width=40)
        entry.pack(padx=20)
        entry.insert(0, default)
        return entry

    name_entry = field("餐廳名稱：", data.get("name") if data else "")
    addr_entry = field("地址：", data.get("address") if data else "")
    price_entry = field("平均價格：", str(data.get("price", "")) if data else "")
    cal_entry = field("卡路里：", str(data.get("calories", "")) if data else "")
    img_entry = field("圖片網址：", data.get("image_url") if data else "")

    tk.Label(form, text="營業時間：", fg=fg_color, bg=bg_color, font=("微軟正黑體", 13, "bold")).pack(pady=(10, 2), anchor="w", padx=20)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hour_entries = {}
    for day in weekdays:
        frame = tk.Frame(form, bg=bg_color)
        frame.pack(anchor="w", padx=30, pady=2)
        day_label = tk.Label(frame, text=f"{day:<10}", fg=fg_color, bg=bg_color, font=("微軟正黑體", 11), width=11, anchor="e")
        day_label.pack(side="left")
        default_hour = data.get("hours", {}).get(day, "") if data else ""
        e = tk.Entry(frame, font=font_main, width=28)
        e.pack(side="left")
        e.insert(0, default_hour)
        hour_entries[day] = e

    def submit():
        new_data = {
            "name": name_entry.get().strip(),
            "address": addr_entry.get().strip(),
            "price": int(price_entry.get()) if price_entry.get().isdigit() else -1,
            "calories": int(cal_entry.get()) if cal_entry.get().isdigit() else -1,
            "image_url": img_entry.get().strip(),
            "hours": {day: hour_entries[day].get().strip() for day in weekdays}
        }
        if not new_data["name"] or not new_data["address"]:
            messagebox.showerror("錯誤", "名稱與地址不可為空")
            return

        global restaurants
        if data:
            for i, r in enumerate(restaurants):
                if r["name"] == data["name"]:
                    restaurants[i] = new_data
                    break
        else:
            if any(r["name"] == new_data["name"] for r in restaurants):
                messagebox.showerror("錯誤", "餐廳名稱已存在")
                return
            restaurants.append(new_data)

        with open('restaurants.json', 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("成功", "資料已儲存")
        form.destroy()
        parent.destroy()
        open_manager_window()

    tk.Button(form, text="💾 確認儲存", command=submit,
              bg="#00cc88", fg="white", font=("微軟正黑體", 12), relief="flat", padx=10, pady=5).pack(pady=20)
