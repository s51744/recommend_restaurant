import random
import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO

class RandomPicker:
    def __init__(self, restaurants, label_info, label_img, btn_pick, root):
        self.restaurants = restaurants
        self.label_info = label_info
        self.label_img = label_img
        self.btn_pick = btn_pick
        self.root = root

        # 動畫參數
        self.interval = 30
        self.max_interval = 500
        self.step = 1.3
        self.current_interval = self.interval

        self.quick_mode = False
        self.filter_open_today = False

        # 篩選條件（預設為最大範圍）
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

        # 僅符合價格與卡路里範圍的餐廳
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
        address = chosen.get('address', '未知')
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
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img.thumbnail((500, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                self.label_img.config(image=photo, text="", bg="black")
                self.label_img.image = photo
            except Exception:
                self.label_img.config(image='', text="⚠️ 圖片載入失敗", bg="black", fg="gray")
                self.label_img.image = None
        else:
            self.label_img.config(image='', text="❌ 沒有圖片", bg="black", fg="gray")
            self.label_img.image = None

    def random_animation(self):
        restaurants_to_pick = self.get_restaurants_to_pick()
        if not restaurants_to_pick:
            self.btn_pick.config(state='normal')
            self.label_info.config(text="😢 沒有符合條件的餐廳")
            self.label_img.config(image='', text="😴", bg="black")
            self.label_img.image = None
            return

        if self.quick_mode:
            chosen = random.choice(restaurants_to_pick)
            self.show_restaurant(chosen)
            self.btn_pick.config(state='normal')
        else:
            if self.current_interval > self.max_interval:
                chosen = random.choice(restaurants_to_pick)
                self.show_restaurant(chosen)
                self.btn_pick.config(state='normal')
                self.current_interval = self.interval
            else:
                chosen = random.choice(restaurants_to_pick)
                self.show_restaurant(chosen)
                self.current_interval = int(self.current_interval * self.step)
                self.root.after(self.current_interval, self.random_animation)

    def start(self):
        self.btn_pick.config(state='disabled')
        self.current_interval = self.interval
        self.random_animation()
