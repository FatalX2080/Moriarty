import flet as ft

import gui
from config import BASE_SIZE, NAME


def main(page: ft.Page):
    win = gui.Win(page, size=BASE_SIZE, name=NAME)


ft.app(main)
