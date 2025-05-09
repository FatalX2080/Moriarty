from .pages import base
from .pages import page0, page1, page2, page3, page4, page5, page6
from .pages import page7, page8, page9, page10, page11, page12


class Factory:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, base_page_args: tuple):
        self._pages_list = []
        self.configure_base_page(base_page_args)
        self.add_pages()

    def get_list(self) -> list:
        return self._pages_list

    def add_pages(self) -> None:
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
            page9.Page9(),
            page10.Page10(),
            page11.Page11(),
            page12.Page12(),
        ]

    def configure_base_page(self, args) -> None:
        base.BasePage.win = args[0]()  # get win
        base.BasePage.win_size = args[1]  # win size
        base.BasePage.page_list = self._pages_list  # list
        base.BasePage.theme = args[2]  # theme
