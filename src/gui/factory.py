from .pages import base, page0, page1, page2, page3, page4, page5, page6, page7, page8


class Factory:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, get_win, win_size):
        self._pages_list = []
        base.BasePage.win = get_win()
        base.BasePage.win_size = win_size
        base.BasePage.page_list = self._pages_list

        self._pages_list += [
            page0.Page0(),
            page1.Page1(),
            page2.Page2(),
            page3.Page3(),
            page4.Page4(),
            page5.Page5(),
            page6.Page6(),
            page7.Page7(),
            page8.Page8(),
        ]

    def get_list(self) -> list:
        return self._pages_list
