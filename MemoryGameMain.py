"""
翻牌記憶遊戲 - 主程式入口點
作者: s1141376 Shi

此檔案作為程式的入口點，只負責初始化和啟動遊戲。
具體的遊戲邏輯分散在以下模組：
  - card.py: Card 類別(卡片元件)
  - game.py: MemoryGame 類別(遊戲主邏輯)
"""

import tkinter as tk
from game import MemoryGame


def main():
    """主程式進入點"""
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()