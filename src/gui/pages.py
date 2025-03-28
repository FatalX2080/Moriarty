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

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read()
        assert self.check()
        self.data["base"] = int(self.data["base"])
        res = self.test.process(self.data["op"], self.data["values"], self.data["base"])
        self.res_text.value = "Result {0}".format(res)
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


class Page2(BasePage):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.test = tests.Task2()

        self.num = ft.TextField(label="Number")
        self.baseX = ft.TextField(label="Base x")
        self.baseAns = ft.TextField(label="Base ans")
        self.lgX = ft.TextField(label="Lg x")
        self.lgAns = ft.TextField(label="Lg ans")

        self.len_text = ft.Text("Fract len", weight=ft.FontWeight.BOLD)
        self.res_text = ft.Text("Result", weight=ft.FontWeight.BOLD)
        self.res_text.spans.append(ft.TextSpan(style=ft.TextStyle(size=9)))

        self._page = self.pinit()

    def pinit(self):
        cont = ft.Container
        col = ft.Column
        row = ft.Row

        c1 = cont(
            content=ft.Text("Test 2", theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
            alignment=ft.alignment.center,
            expand=True,
        )

        num_row = row(controls=[self.num], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        res_row = row(
            controls=[self.len_text, ft.Button(text="Evaluate", on_click=self.process)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        task_content = [
            num_row,
            self.baseX,
            self.baseAns,
            self.lgX,
            self.lgAns,
            ft.Divider(height=1),
            res_row,
            self.res_text
        ]
        top_part = cont(col([cont(c1), cont(col(task_content))]))
        bottom_part = cont(self.bottom_bar)

        main_col = col(controls=[top_part, bottom_part], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        return cont(content=main_col, expand=True)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read()
        assert self.check()
        self.data["base_x"] = int(self.data["base_x"])
        self.data["base_ans"] = int(self.data["base_ans"])
        self.data["lg_x"] = float(self.data["lg_x"])
        self.data["lg_ans"] = float(self.data["lg_ans"])
        res = self.test.process(
            self.data["x"],
            self.data["base_x"],
            self.data["base_ans"],
            self.data["lg_x"],
            self.data["lg_ans"]
        )
        self.len_text.value = "Fract len {0} -> {1}".format(res[0], res[1])
        self.res_text.value = "Result {0}".format(res[3][0])
        self.res_text.spans[0].text = "{0}".format(res[2])
        self._page.update()

    def read(self):
        self.data["x"] = self.num.value
        self.data["base_x"] = self.baseX.value
        self.data["base_ans"] = self.baseAns.value
        self.data["lg_x"] = self.lgX.value
        self.data["lg_ans"] = self.lgAns.value

    def check(self) -> bool:
        try:
            x = self.data["x"]
            base_x = self.data["base_x"]
            base_ans = self.data["base_ans"]
            lg_x = self.data["lg_x"]
            lg_ans = self.data["lg_ans"]
            if any([i == '' for i in [x, base_x, base_ans, lg_x, lg_ans]]):
                return False
            int(base_x)
            int(base_ans)
            float(lg_x)
            float(lg_ans)
        except ValueError:
            return False
        return True
