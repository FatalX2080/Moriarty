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


class TaskBasePage(BasePage):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self.index = 0
        self.data = {}

    def join_top(self, task_block) -> ft.Container:
        col = ft.Column
        cont = ft.Container

        title = cont(
            content=ft.Text(
                "Test {0}".format(self.index),
                theme_style=ft.TextThemeStyle.DISPLAY_LARGE
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
        return cont(col([title, cont(col(task_block))]))

    def join_page(self, top_part):
        return ft.Container(
            content=ft.Column(
                controls=[top_part, self.bottom_bar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            expand=True
        )

    def read(self, entries: dict):
        self.data.clear()
        for k in entries.keys(): self.data[k] = entries[k].value


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


# ----------------------------------------------------------------------------------------------------------


class Page1(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 1
        self.test = tests.Task1()

        rbuttons = ft.Row(
            [
                ft.Container(
                    ft.Radio(value=opt, label=opt),
                    expand=True,
                    alignment=ft.alignment.center,
                )
                for opt in ["+", "-", "*", "//"]
            ],
            expand=True,
        )
        self.sign = ft.RadioGroup(content=rbuttons, value="+")
        self.val1_field = ft.TextField(label="Operand 1")
        self.val2_field = ft.TextField(label="Operand 2")
        self.base_field = ft.TextField(label="Base")
        self.res_text = ft.Text("Result", weight=ft.FontWeight.BOLD)

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
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
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        rdict = {"op": self.sign, "v1": self.val1_field, "v2": self.val2_field, "base": self.base_field}
        self.read(rdict)
        assert self.check()
        self.data["base"] = int(self.data["base"])
        res = self.test.process(self.data["op"], (self.data["v1"], self.data["v2"]), self.data["base"])
        self.res_text.value = "Result {0}".format(res)
        self._page.update()

    def check(self) -> bool:
        try:
            v1 = self.data["v1"]
            v2 = self.data["v2"]
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


class Page2(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 2
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
        row = ft.Row
        res_row = row(
            controls=[self.len_text, ft.Button(text="Evaluate", on_click=self.process)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        task_content = [
            self.num,
            self.baseX,
            self.baseAns,
            self.lgX,
            self.lgAns,
            ft.Divider(height=1),
            res_row,
            self.res_text
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({
            "x": self.num, "base_x": self.baseX, "base_ans": self.baseAns,
            "lg_x": self.lgX, "lg_ans": self.lgAns
        })
        assert self.check()
        self.data["base_x"] = int(self.data["base_x"])
        self.data["base_ans"] = int(self.data["base_ans"])
        self.data["lg_x"] = float(self.data["lg_x"])
        self.data["lg_ans"] = float(self.data["lg_ans"])
        res = self.test.process(*self.data.values())
        self.len_text.value = "Fract len {0} -> {1}".format(res[0], res[1])
        self.res_text.value = "Result {0}".format(res[3][0])
        self.res_text.spans[0].text = "{0}".format(res[2])
        self._page.update()

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


class Page3(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 3
        self.data = {}
        self.test = tests.Task3()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.SDNF_text = ft.Text("SDNF", weight=ft.FontWeight.BOLD)
        self.SKNF_text = ft.Text("SKNF", weight=ft.FontWeight.BOLD)

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[self.SDNF_text, ft.Button(text="Evaluate", on_click=self.process)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.count,
            self.res,
            ft.Divider(height=1),
            res_row,
            self.SKNF_text
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"count": self.count, "res": self.res})
        assert self.check()
        self.data["count"] = int(self.data["count"])
        self.data["res"] = tuple([int(r) for r in list(self.data["res"])])
        res = self.test.process(*self.data.values())
        # TODO не влезает
        self.SDNF_text.value = "SDNF {0}".format(res[0])
        self.SKNF_text.value = "SKNF {0}".format(res[1])

        self._page.update()

    def check(self) -> bool:
        try:
            x = self.data["count"]
            res = self.data["res"]
            if any([i == '' for i in [x, res]]):
                return False
            int(x)
            if len(res) != 2 ** int(x):
                return False
            if any([int(r) != 0 and int(r) != 1 for r in list(res)]):
                return False
        except ValueError:
            return False
        return True
