import random
import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import pygame
import threading

# 初始化 pygame mixer
pygame.mixer.init()

class RandomPicker:
    def __init__(self, restaurants, label_info, label_img, btn_pick, root):
        self.restaurants = restaurants
        self.label_info = label_info
        self.label_img = label_img
        self.btn_pick = btn_pick
        self.root = root
        self.last_picked_name = None
        self.last_picked_address = None
        self.root = root

        self.interval = 88
        self.max_interval = 1111
        self.step = 1.3
        self.current_interval = self.interval

        self.quick_mode = False
        self.filter_open_today = False

        self.calorie_min = 0
        self.calorie_max = float("inf")
        self.price_min = 0
        self.price_max = float("inf")

    def set_quick_mode(self, quick: bool):
        self.quick_mode = quick

    def set_filter_open_today(self, filter_open: bool):
        self.filter_open_today = filter_open

    def set_calorie_range(self, cal_min: int, cal_max: int):
        self.calorie_min = cal_min
        self.calorie_max = cal_max

    def set_price_range(self, price_min: int, price_max: int):
        self.price_min = price_min
        self.price_max = price_max

    def get_restaurants_to_pick(self):
        today = datetime.datetime.today().strftime("%A")
        filtered = [
            r for r in self.restaurants
            if self.calorie_min <= r.get("calories", 0) <= self.calorie_max
            and self.price_min <= r.get("price", 0) <= self.price_max
        ]
        if self.filter_open_today:
            filtered = [
                r for r in filtered
                if r.get("hours", {}).get(today, "") not in ["休息", "不明"]
            ]
        return filtered

    def show_restaurant(self, chosen):
        today = datetime.datetime.today().strftime("%A")
        hours = chosen.get('hours', {})
        open_status = hours.get(today, "不明")
        if open_status == "休息":
            open_text = "🕒 今天休息"
        elif open_status == "不明":
            open_text = "🕒 營業時間未知"
        else:
            open_text = f"🕒 今天營業時間：{open_status}"

        name = chosen.get('name', '未知')
        self.last_picked_name = name
        address = chosen.get('address', '未知')
        self.last_picked_address = address
        price = chosen.get('price', '未知')
        calories = chosen.get('calories', '未知')

        info_text = (
            f"【 餐廳名稱 】\n　{name}\n"
            f"【 地　　址 】\n　{address}\n"
            f"【 今日營業 】\n　{open_text}\n"
            f"【 平均價格 】\n　NT${price} 元\n"
            f"【 卡 路 里 】\n　約 {calories} 大卡"
        )
        self.label_info.config(
            text=info_text,
            font=("微軟正黑體", 13),
            justify="left",
            anchor="w",
            wraplength=400,
            pady=10
        )

        url = chosen.get('image_url', '')
        if url:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                img.thumbnail((500, 400), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.label_img.config(image=photo, text="", bg="black")
                self.label_img.image = photo
            except:
                self.label_img.config(image='', text="⚠️ 圖片載入失敗", bg="black", fg="gray")
                self.label_img.image = None
        else:
            self.label_img.config(image='', text="❌ 沒有圖片", bg="black", fg="gray")
            self.label_img.image = None

    def start(self, after_spin_callback=None):
        self.after_spin_callback = after_spin_callback
        self.btn_pick.config(state='disabled')
        self.current_interval = self.interval
        self.slow_left = None

        restaurants_to_pick = self.get_restaurants_to_pick()
        if not restaurants_to_pick:
            self.btn_pick.config(state='normal')
            self.label_info.config(
                text="😩 沒有符合條件的餐廳！\n\n你太挑了啦！再不放寬一點，連泡麵都沒得吃 🍜",
                font=("微軟正黑體", 13),
                justify="left",
                anchor="w",
                wraplength=400,
                pady=10
            )
            try:
                img_url = "https://www.niusnews.com/upload/posts/po5_29953_1421316750.jpg"
                response = requests.get(img_url)
                img = Image.open(BytesIO(response.content))
                img.thumbnail((500, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.label_img.config(image=photo, text="", bg="black")
                self.label_img.image = photo
            except:
                self.label_img.config(image='', text="⚠️ 圖片載入失敗", bg="black", fg="gray")
                self.label_img.image = None

            def _cry():
                try:
                    pygame.mixer.Sound("sounds/cry.mp3").play()
                except:
                    pass
            threading.Thread(target=_cry, daemon=True).start()

            if self.after_spin_callback:
                self.after_spin_callback()
            return

        self.random_animation()


    def random_animation(self):
        restaurants_to_pick = self.get_restaurants_to_pick()
        if not restaurants_to_pick:
            self.btn_pick.config(state='normal')
            self.label_info.config(
                text="😩 沒有符合條件的餐廳！\n\n你太挑了啦！再不放寬一點，連泡麵都沒得吃 🍜",
                font=("微軟正黑體", 13),
                justify="left",
                anchor="w",
                wraplength=400,
                pady=10
            )
            self.label_img.config(image='', text="⚠️ 沒有圖片", bg="black", fg="gray")
            return

        # 快速模式：直接抽
        if self.quick_mode:
            chosen = random.choice(restaurants_to_pick)
            self.show_restaurant(chosen)
            self.btn_pick.config(state='normal')
            self.play_ding()
            if self.after_spin_callback:
                self.after_spin_callback()
            return

        # 慢速模式流程
        if self.current_interval >= self.max_interval:
            # 最終前一張（max_interval），先播放這張後再等久一點
            chosen = random.choice(restaurants_to_pick)
            self.show_restaurant(chosen)
            self.play_tick()

            #停久一點再播最終張
            def show_final():
                final_choice = random.choice(restaurants_to_pick)
                self.show_restaurant(final_choice)
                self.play_ding()
                self.btn_pick.config(state='normal')
                if self.after_spin_callback:
                    self.after_spin_callback()

            self.root.after(1888, show_final)
            return

        # 一般過程：持續遞增間隔
        chosen = random.choice(restaurants_to_pick)
        self.show_restaurant(chosen)
        self.play_tick()
        self.current_interval = int(self.current_interval * self.step)
        self.root.after(self.current_interval, self.random_animation)




    def play_tick(self):
        def _tick():
            try:
                pygame.mixer.Sound("sounds/ding2.wav").play()
            except Exception as e:
                print(f"spin 播放失敗: {e}")
        threading.Thread(target=_tick, daemon=True).start()

    def stop_tick(self):
        try:
            pygame.mixer.stop()
        except:
            pass

    def play_ding(self):
        def _ding():
            try:
                pygame.mixer.Sound("sounds/ok.wav").play()
            except:
                pass
        threading.Thread(target=_ding, daemon=True).start()