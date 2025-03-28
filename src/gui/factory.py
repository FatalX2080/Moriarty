from .pages import Page0, Page1, BasePage


class Factory:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, get_win):
        self._pages_list = []
        BasePage.win = get_win()
        BasePage.page_list = self._pages_list

        self._pages_list.append(Page0())
        self._pages_list.append(Page1())

    def get_list(self) -> list:
        return self._pages_list
