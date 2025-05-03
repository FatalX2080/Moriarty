import flet as ft
from config import BASE_SIZE

from .factory import Factory


# TODO 5-7 нижняя полоса съехала
# TODO в сборке v3 сделать базирование на theme colors

class Win:
    def __init__(self, page):
        self.page = page
        self.page.title = "Moriarty"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        #                               ------!TEST!------
        skale = 3
        self.page.window.width = BASE_SIZE[0] // skale
        self.page.window.height = BASE_SIZE[1] // skale
        #                               ------!TEST!------
        w_size = (self.page.window.width, self.page.window.height)

        self._win = ft.Container(expand=True)
        factory = Factory(self.get_win, w_size)
        self.pages_list = factory.get_list()

        self.pages_list[0].render()
        self.page.update()

    # ------------------------------------------------------------------------------------------------------
    def get_win(self):
        return self._win
