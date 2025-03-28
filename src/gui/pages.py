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
        self._page = None

    def render(self):
        BasePage.win.content = self._page


# ----------------------------------------------------------------------------------------------------------

class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self._page = self.pinit()

    def pinit(self):
        return ft.Column(
            controls=[ft.Text("Template"), self.bottom_bar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


class Page1(BasePage):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.test = tests.Task1()

        self.sign = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Container(
                        ft.Radio(value=opt, label=opt),
                        expand=True,
                        alignment=ft.alignment.center,
                    )
                    for opt in ["+", "-", "*", "//"]
                ],
                expand=True,
            ),
            value="+",
        )
        self.val1_field = ft.TextField(label="Operand 1")
        self.val2_field = ft.TextField(label="Operand 2")
        self.base_field = ft.TextField(label="Base")
        self.res_text = ft.Text("Result", weight=ft.FontWeight.BOLD)

        self._page = self.pinit()

    def pinit(self):
        cont = ft.Container
        col = ft.Column
        row = ft.Row

        c1 = cont(
            content=ft.Text("Test 1", theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
            alignment=ft.alignment.center,
            expand=True,
        )
        res_row = row(
            controls=[self.res_text, ft.Button(text="Evaluate", on_click=self.process)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.val1_field,
            self.val2_field,
            self.base_field,
            ft.Text("Operation"),
            self.sign,
            ft.Divider(height=1),
            res_row
        ]
        top_part = cont(col([cont(c1), cont(col(task_content))]))
        bottom_part = cont(self.bottom_bar)

        main_col = col(
            controls=[top_part, bottom_part],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        return cont(content=main_col, expand=True)

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
