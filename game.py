"""
MemoryGame 類別 - 翻牌記憶遊戲的主邏輯
作者: s1141376 Shi
"""

import tkinter as tk
from tkinter import messagebox
import random
import time
from pathlib import Path
from card import Card


class MemoryGame:
    """
    翻牌記憶遊戲主類別
    管理遊戲邏輯、計時器、卡片配對等功能
    """

    def __init__(self, root):
        """
        初始化遊戲

        參數:
            root: Tkinter 主視窗
        """
        self.root = root

        self.root.title(
            "翻牌記憶遊戲, S1141376 Shi"
        )

        self.root.geometry(
            "700x550"
        )

        # 遊戲狀態
        self.first_card = None
        self.second_card = None
        self.lock = False
        self.start_time = time.time()

        self.card_images = self.load_card_images()

        # 上方資訊框架
        top_frame = tk.Frame(root)
        top_frame.pack()

        self.time_label = tk.Label(
            top_frame,
            text="時間:0 秒",
            font=("Arial", 16)
        )
        self.time_label.pack()

        # 卡片區框架
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.card_list = []

        self.create_cards()
        self.update_timer()

    def load_card_images(self):
        """載入卡片圖像資源"""
        images = {}
        image_dir = Path(__file__).resolve().parent / "poker_images"
        value_map = {
            "A": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
        }

        back_path = image_dir / "pokerbk.jpg"
        if not back_path.exists():
            raise FileNotFoundError(
                f"找不到卡片背面圖像: {back_path}"
            )

        try:
            from PIL import Image, ImageTk
        except ImportError as exc:
            raise ImportError(
                "請安裝 Pillow 才能載入 JPG 卡片圖像。" \
                "(pip install pillow)"
            ) from exc

        back_image = ImageTk.PhotoImage(
            Image.open(back_path).resize((100, 140), Image.Resampling.LANCZOS)
        )

        for value, index in value_map.items():
            if value == "K":
                continue

            image_path = image_dir / f"poker{index}.jpg"
            if not image_path.exists():
                raise FileNotFoundError(
                    f"找不到卡片正面圖像: {image_path}"
                )

            images[value] = ImageTk.PhotoImage(
                Image.open(image_path).resize((100, 140), Image.Resampling.LANCZOS)
            )

        images["BACK"] = back_image
        return images

    def create_cards(self):
        """建立遊戲卡片"""
        cards = [
            "A", "2", "3", "4",
            "5", "6", "7", "8",
            "9", "10", "J", "Q"
        ]

        # 複製卡片以建立配對
        cards = cards * 2

        # 洗牌
        random.shuffle(cards)

        self.card_list = []
        index = 0

        # 建立 4x6 的卡片網格
        for r in range(4):
            for c in range(6):
                card = Card(
                    self.frame,
                    cards[index],
                    self,
                    front_image=self.card_images[cards[index]],
                    back_image=self.card_images["BACK"]
                )

                card.grid(
                    row=r,
                    column=c,
                    padx=5,
                    pady=5
                )

                self.card_list.append(card)
                index += 1

    def select_card(self, card):
        """
        處理卡片被選中

        參數:
            card: 被選中的卡片物件
        """
        # 檢查遊戲是否被鎖定
        if self.lock:
            return

        # 檢查卡片是否已翻開
        if card.is_flipped:
            return

        # 檢查卡片是否已配對
        if card.is_matched:
            return

        # 顯示卡片正面
        card.show_front()

        # 記錄第一張卡片
        if self.first_card is None:
            self.first_card = card
            return

        # 記錄第二張卡片並檢查配對
        self.second_card = card
        self.lock = True

        # 3秒後檢查是否配對
        self.root.after(
            3000,
            self.check_match
        )

    def check_match(self):
        """檢查兩張卡片是否配對"""
        if (
            self.first_card.value
            ==
            self.second_card.value
        ):
            # 配對成功
            self.first_card.clear_card()
            self.second_card.clear_card()
        else:
            # 配對失敗，翻回背面
            self.first_card.show_back()
            self.second_card.show_back()

        # 重置選擇
        self.first_card = None
        self.second_card = None
        self.lock = False

        # 檢查遊戲是否完成
        self.check_game_finish()

    def check_game_finish(self):
        """檢查遊戲是否完成"""
        finished = True

        for card in self.card_list:
            if not card.is_matched:
                finished = False
                break

        if finished:
            elapsed = int(
                time.time()
                - self.start_time
            )

            result = messagebox.askyesno(
                "遊戲完成",
                f"恭喜過關！\n"
                f"花費:{elapsed}秒\n"
                f"重新開始?"
            )

            if result:
                self.restart()
            else:
                self.root.destroy()

    def update_timer(self):
        """更新計時器"""
        elapsed = int(
            time.time()
            - self.start_time
        )

        self.time_label.config(
            text=f"時間:{elapsed} 秒"
        )

        if not self.is_finished():
            self.root.after(
                1000,
                self.update_timer
            )

    def is_finished(self):
        """檢查是否所有卡片都已配對"""
        for card in self.card_list:
            if not card.is_matched:
                return False
        return True

    def restart(self):
        """重新開始遊戲"""
        self.frame.destroy()

        self.frame = tk.Frame(
            self.root
        )

        self.frame.pack()

        self.start_time = time.time()

        self.first_card = None
        self.second_card = None
        self.lock = False

        self.create_cards()
        self.update_timer()
