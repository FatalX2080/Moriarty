import flet as ft
from tests import Task2

from .base import TaskBasePage, BasicChecks


class Page2(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 2
        self.data = {}
        self.test = Task2()

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
            controls=[self.len_text, self.evaluate_btn],
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
        try:
            self.check()
        except AssertionError:
            pass
        else:
            res = self.test.process(*self.data.values())
            self.len_text.value = "Fract len {0} -> {1}".format(res[0], res[1])
            self.res_text.value = "Result {0}".format(res[3][0])
            self.res_text.spans[0].text = "{0}".format(res[2])
            self._page.update()

    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array(vals)

        assert eng.is_int(vals[1])
        assert eng.is_int(vals[2])
        assert eng.borders(vals[1], (2, 16))
        assert eng.borders(vals[2], (2, 16))

        assert eng.include(vals[0], ".")

        assert eng.is_float(vals[3])
        assert eng.is_float(vals[4])

        assert eng.grounds(vals[0], vals[1])

        self.data["base_x"] = int(self.data["base_x"])
        self.data["base_ans"] = int(self.data["base_ans"])
        self.data["lg_x"] = float(self.data["lg_x"])
        self.data["lg_ans"] = float(self.data["lg_ans"])
