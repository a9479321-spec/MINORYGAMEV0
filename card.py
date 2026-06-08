"""
Card 類別 - 翻牌記憶遊戲的卡片元件
作者: s1141376 Shi
"""

import tkinter as tk

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None


class Card(tk.Button):
    """
    卡片類別
    繼承 tk.Button，表示遊戲中的單張卡片
    """

    def __init__(self, master, value, game, front_image=None, back_image=None, **kwargs):
        """
        初始化卡片

        參數:
            master: 父容器
            value: 卡片的數值(例如: "A", "2", "3"等)
            game: 遊戲物件的參考
            front_image: 正面圖像
            back_image: 背面圖像
            **kwargs: 其他 Button 參數
        """
        super().__init__(
            master,
            width=8,
            height=4,
            font=("Arial", 16),
            command=self.click_card,
            **kwargs
        )

        self.value = value
        self.game = game
        self.front_image = front_image
        self.back_image = back_image

        self.is_flipped = False
        self.is_matched = False

        self.show_back()

    def show_back(self):
        """顯示卡片背面"""
        if self.is_matched:
            return

        if self.back_image is not None:
            self.config(image=self.back_image, text="")
        else:
            self.config(text="❓", image="")

        self.config(state="normal")
        self.is_flipped = False

    def show_front(self):
        """顯示卡片正面"""
        if self.front_image is not None:
            self.config(image=self.front_image, text="")
        else:
            self.config(text=self.value, image="")

        self.is_flipped = True

    def clear_card(self):
        """清除卡片(配對成功時調用)"""
        self.config(
            image="",
            text="",
            state="disabled",
            bg="lightgray"
        )
        self.is_matched = True

    def click_card(self):
        """卡片被點擊時的處理"""
        self.game.select_card(self)
