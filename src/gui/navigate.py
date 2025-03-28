import flet as ft


class MainMenu:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, win, pages_list):
        self.__win = win
        self.__pages_list = pages_list
        self.NavDraw = None
        self.generate()

    def generate(self):
        nav = ft.NavigationDrawerDestination
        home_link = [nav(label="Home", icon=ft.Icons.HOME)]
        nv_list = home_link + [nav(label="Test {0}".format(index)) for index in range(1, 14)]
        self.NavDraw = ft.NavigationDrawer(controls=nv_list, on_change=self.event)

    def event(self, e=None):
        try:
            self.__win.content = None
            page_iex = e.control.selected_index
            page = self.__pages_list[page_iex]
            if page is None:  page = self.__pages_list[0]
            page.render()
            e.control.page.update()
        except IndexError:
            raise Exception("Index out of range")


class BottomBar:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, win, plist):
        self.menu = MainMenu(win, plist)
        self.NavBar = None
        self.generate()

    def generate(self):
        dest = ft.NavigationBarDestination
        nav_bar_buttons = [
            dest(icon=ft.Icons.HOME, label="Menu"),
            dest(icon=ft.Icons.INFO, label="Test info"),
        ]
        bar = ft.NavigationBar(destinations=nav_bar_buttons, on_change=self.event)
        self.NavBar = ft.Pagelet(navigation_bar=bar, content=ft.Container(), height=300, )

    def event(self, e=None):
        iex = e.control.selected_index
        match iex:
            case 0:
                self.open_navigate(e)
            case 1:
                print("Типо информация о странице")

    def open_navigate(self, e):
        e.control.page.drawer = self.menu.NavDraw
        self.menu.NavDraw.open = True
        e.control.page.update()
