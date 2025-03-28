import flet as ft
from .factory import Factory


class Win:
    def __init__(self, page):
        self.page = page
        self.page.title = "QVM"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        #                               ------!TEST!------
        base_size = (2400, 1080)
        skale = 3
        self.page.window.height = base_size[0] // skale
        self.page.window.width = base_size[1] // skale
        #                               ------!TEST!------

        self._win = ft.Container(expand=True)
        self.pages_list = Factory(self.get_win).get_list()

        self.pages_list[0].render()
        self.page.update()

    # ------------------------------------------------------------------------------------------------------
    def get_win(self):
        return self._win
