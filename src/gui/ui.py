import flet as ft
from .factory import Factory


class Win:


    def __init__(self, page):
        self.page = page
        self.page.title = "QVM"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        self._win = ft.Container()
        f = Factory(self.switch_page)
        self.pages_list = f.get_list()

        self.pages_list[0].render(self.get_win)
        self.page.update()

    # ------------------------------------------------------------------------------------------------------
    def switch_page(self, e=None):
        try:
            self._win.content = None
            page_iex = e.control.selected_index
            page = self.pages_list[page_iex]
            if page is None:
                page = self.pages_list[0]

            page.render(self.get_win)
            e.control.page.update()
        except IndexError:
            raise Exception("Index out of range")

    # ------------------------------------------------------------------------------------------------------
    def get_win(self):
        return self._win
