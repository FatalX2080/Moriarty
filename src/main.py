import flet as ft

import gui


def main(page: ft.Page):
    win = gui.Win(page)
    page.add(win.get_win())


ft.app(main)
# flet build apk
