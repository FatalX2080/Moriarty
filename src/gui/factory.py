from .pages import BasePage, Page0, Page1, Page2, Page3, Page4, Page7


class Factory:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, get_win, win_size):
        self._pages_list = []
        BasePage.win = get_win()
        BasePage.win_size = win_size
        BasePage.page_list = self._pages_list

        self._pages_list += [
            Page0(),
            Page1(),
            Page2(),
            Page3(),
            Page4(),
                Page0(),
                Page0(),
            Page7(),
        ]

    def get_list(self) -> list:
        return self._pages_list
