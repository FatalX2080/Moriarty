import flet as ft

import gui
from config import BASE_SIZE, NAME


def main(page: ft.Page):
    win = gui.Win(page, size=BASE_SIZE, name=NAME)
    page.add(win.get_win())


ft.app(main)
