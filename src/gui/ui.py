from typing import Optional

import flet as ft

from .factory import Factory


# TODO доделать нормальную настройку размера

class Win:
    def __init__(self, page, size: Optional[tuple], name: str):
        self.page = page
        self.page.title = name
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.set_size(size)
        self._win = ft.Container(expand=True)

        self.page.update()

        size = (self.page.window.width, self.page.window.height)
        base_page_config = (self.get_win, size, self.define_theme())
        factory = Factory(base_page_config)
        self.pages_list = factory.get_list()

        self.pages_list[0].render()
        self.page.update()

    # ------------------------------------------------------------------------------------------------------
    def get_win(self):
        return self._win

    def set_size(self, page_size):
        if page_size:
            self.page.window.width = page_size[0] // 3
            self.page.window.height = page_size[1] // 3

    def define_theme(self) -> int:
        theme = 1  # 1 - Bright | 0 - Dark
        t_mode = self.page.theme_mode
        if t_mode.value == "system":
            theme = self.page.platform_brightness == ft.Brightness.LIGHT
        elif t_mode.vslue == "dark":
            theme = 0
        return theme
