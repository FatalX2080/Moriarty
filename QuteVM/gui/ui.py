import flet as ft
from .pages import Factory


class Win:


    def __init__(self, page):
        self.page = page
        self.page.title = "QVM"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        self._win = None
        self.__win_tool = (self.set_win, self.get_win)
        self.pages_list = Factory(self.switch_page).get_list()

        self.pages_list[0].render(*self.__win_tool)
        self.page.update()

    # ------------------------------------------------------------------------------------------------------
    def switch_page(self, e=None):
        try:
            page = self.pages_list[e.control.selected_index]
            if page is None:
                page = self.pages_list[0]

            page.render(*self.__win_tool)
            self.page.update()
        except IndexError:
            raise Exception("Index out of range")

    # ------------------------------------------------------------------------------------------------------
    def set_win(self, new_win=None) -> None:
        self._win = new_win

    def get_win(self):
        return self._win
