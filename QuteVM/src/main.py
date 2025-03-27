import flet as ft
from gui.ui import Win

def main(page: ft.Page):
    win = Win(page)

    page.add(win.get_win())

ft.app(main)
