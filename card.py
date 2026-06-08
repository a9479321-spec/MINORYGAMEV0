"""
Card 類別 - 翻牌記憶遊戲的卡片元件
作者: s1141376 Shi
"""

import tkinter as tk


class Card(tk.Button):
    """
    卡片類別
    繼承 tk.Button，表示遊戲中的單張卡片
    """

    def __init__(self, master, value, game, **kwargs):
        """
        初始化卡片

        參數:
            master: 父容器
            value: 卡片的數值(例如: "A", "2", "3"等)
            game: 遊戲物件的參考
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

        self.is_flipped = False
        self.is_matched = False

        self.show_back()

    def show_back(self):
        """顯示卡片背面"""
        if not self.is_matched:
            self.config(
                text="❓",
                state="normal"
            )
            self.is_flipped = False

    def show_front(self):
        """顯示卡片正面"""
        self.config(
            text=self.value
        )
        self.is_flipped = True

    def clear_card(self):
        """清除卡片(配對成功時調用)"""
        self.config(
            text="",
            state="disabled",
            bg="lightgray"
        )
        self.is_matched = True

    def click_card(self):
        """卡片被點擊時的處理"""
        self.game.select_card(self)
