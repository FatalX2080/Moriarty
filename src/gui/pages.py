import flet as ft
from .navigate import BottomBar
import tests


class BasePage:
    win = None
    page_list = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        bar = BottomBar(BasePage.win, BasePage.page_list)
        self.bottom_bar = bar.NavBar


# ----------------------------------------------------------------------------------------------------------
class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self._page = self.pinit()

    def render(self):
        BasePage.win.alignment = ft.alignment.center
        BasePage.win.content = self._page

    def pinit(self):
        return ft.Column(controls=[
            ft.Text("Template"),
            self.bottom_bar
        ])


class Page1(BasePage):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.test = tests.Task1()

        self.sign = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value="+", label="+"),
                    ft.Radio(value="-", label="-"),
                    ft.Radio(value="*", label="*"),
                    ft.Radio(value="/", label="/"),
                ]
            ), value="+"
        )
        self.val1_field = ft.TextField(label="Num 1")
        self.val2_field = ft.TextField(label="Num 2")
        self.base_field = ft.TextField(label="Base")
        self.res_text = ft.Text("Result")

        self._page = self.pinit()

    def pinit(self):
        return ft.Column([
            ft.Text("Test 1", theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
            self.val1_field,
            self.val2_field,
            self.base_field,
            ft.Text("Operation"),
            self.sign,
            self.res_text,
            ft.Button(text="Evaluate", on_click=self.process),
            self.bottom_bar
        ])

    def render(self):
        BasePage.win.content = self._page

    # ------------------------------------------------------------------------------------------------------
    def process(self, e):
        self.read()
        assert self.check()
        self.data["base"] = int(self.data["base"])
        res = self.test.process(self.data["op"], self.data["values"], self.data["base"])
        self.res_text.value = "Result: {0}".format(res)
        self._page.update()

    def read(self):
        self.data["op"] = self.sign.value
        self.data["values"] = (self.val1_field.value, self.val2_field.value)
        self.data["base"] = self.base_field.value

    def check(self) -> bool:
        try:
            v1 = self.data["values"][0]
            v2 = self.data["values"][1]
            b = self.data["base"]
            if v1 == "":
                return False
            if v2 == "":
                return False
            if b == "":
                return False
            int(v1)
            int(v2)
            int(v2)
            if max(v1) >= b or max(v2) >= b:
                return False
        except ValueError:
            return False
        return True
