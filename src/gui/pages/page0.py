import flet as ft

from .base import BasePage


class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self.index = 0
        self._page = self.pinit()

    def pinit(self):
        return ft.Column(
            controls=[ft.Text("Template"), self.bottom_bar.NavBar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
