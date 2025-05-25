import random
import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO

class RandomPicker:
    def __init__(self, restaurants, label_info, label_img, label_open, label_price, label_calories, btn_pick, root):
        self.restaurants = restaurants
        self.label_info = label_info
        self.label_img = label_img
        self.label_open = label_open
        self.label_price = label_price
        self.label_calories = label_calories
        self.btn_pick = btn_pick
        self.root = root

        #動畫參數
        self.interval = 30 #初始間隔時間（毫秒）
        self.max_interval = 500 #最大間隔時間（動畫結束時的速度）
        self.step = 1.3 #每次間隔變慢的倍率
        self.current_interval = self.interval

        #是否快速模式 (True = 立刻出結果)
        self.quick_mode = False

    def set_quick_mode(self, quick: bool):
        self.quick_mode = quick

    def show_restaurant(self, chosen):
        info = f"餐廳：{chosen['name']}\n地址：{chosen['address']}"
        self.label_info.config(text=info)

        today = datetime.datetime.today().strftime("%A")
        hours = chosen.get('hours', {})
        open_status = hours.get(today, "不明")
        if open_status == "休息":
            open_text = "今天休息"
        elif open_status == "不明":
            open_text = "營業時間未知"
        else:
            open_text = f"今天營業時間{open_status}"
        self.label_open.config(text="營業狀態：" + open_text)
        
        price = chosen.get('price', '不清楚')
        self.label_price.config(text=f"平均價格：{price} 元")
        
        calories = chosen.get('calories', '未知')
        self.label_calories.config(text=f"卡路里：{calories} 大卡")

        url = chosen.get('image_url', '')
        if url:
            try:
                response = requests.get(url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                max_size = (500, 400)
                img.thumbnail(max_size, Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)

                self.label_img.config(image=photo, text='')
                self.label_img.image = photo
            except Exception:
                self.label_img.config(image='', text="圖片載入失敗")
                self.label_img.image = None
        else:
            self.label_img.config(image='', text="沒有圖片網址")
            self.label_img.image = None

    def random_animation(self):
        if self.quick_mode:
            # 快速模式直接顯示
            chosen = random.choice(self.restaurants)
            self.show_restaurant(chosen)
            self.btn_pick.config(state='normal')
        else:
            # 慢速動畫模式
            if self.current_interval > self.max_interval:
                chosen = random.choice(self.restaurants)
                self.show_restaurant(chosen)
                self.btn_pick.config(state='normal')
                self.current_interval = self.interval
            else:
                chosen = random.choice(self.restaurants)
                self.show_restaurant(chosen)
                self.current_interval = int(self.current_interval * self.step)
                self.root.after(self.current_interval, self.random_animation)

    def start(self):
        self.btn_pick.config(state='disabled')
        self.current_interval = self.interval
        self.random_animation()
