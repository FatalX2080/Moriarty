import flet as ft
from config import TEST_LIST


# ----------------------------------------------------------------------------------------------------------


class BasePage:
    def __init__(self):
        self._page = None
        self.index = -1

        self.navigation = ft.NavigationDrawer(controls=BasePage.__generate_pages())

    def open_navigate(self, e):
        e.control.page.drawer = self.navigation
        self.navigation.open = True
        e.control.page.update()

    def set_switch_event(self, switch_func):
        self.navigation.on_change = switch_func

    @staticmethod
    def __generate_pages():
        nav = ft.NavigationDrawerDestination
        navigate_list = [nav(label="Home", icon=ft.Icons.HOME)]
        return navigate_list + [nav(label="Test {0}".format(index)) for index in TEST_LIST]

    # ------------------------------------------------------------------------------------------------------
    def get_page(self):
        return self._page

    def get_index(self) -> int:
        return self.index


class Factory:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, sw_event):
        self._active_pages = TEST_LIST
        self._pages_list = []

        self._pages_list.append(Page0())

        self.base_config(sw_event)

    def base_config(self, sw_event):
        expand_lit = self._active_pages + [0]
        for iex, page in enumerate(self._pages_list):
            if page.get_index() not in expand_lit:
                self._pages_list[iex] = None
            else:
                page.set_switch_event(sw_event)

    def get_list(self) -> list:
        return self._pages_list


# ----------------------------------------------------------------------------------------------------------
class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self.index = 0
        self._page = ft.Column([
            ft.ElevatedButton("Open end drawer", on_click=self.open_navigate),
        ])

    def render(self, s, g):
        s(ft.Container(alignment=ft.alignment.center))
        g().content = self._page
