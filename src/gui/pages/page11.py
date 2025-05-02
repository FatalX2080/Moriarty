import flet as ft
from tests import Task11

from .base import TaskBasePage, BasicChecks


class Page11(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 11
        self.data = {}
        self.test = Task11()

        self.num1_p1 = ft.TextField(label="Operand 1")
        self.num2_p1 = ft.TextField(label="Operand 2")

        self.num1_p2 = ft.TextField(label="Operand 1")
        self.num2_p2 = ft.TextField(label="Operand 2")

        self.code = ft.Dropdown(
            label="code", autofocus=True, value="o",
            options=[ft.dropdown.Option("p"), ft.dropdown.Option("d"), ft.dropdown.Option("o")],
        )

        self.view = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=self.win_size[0],
            height=self.win_size[1] * 0.35,
            spacing=10,
        )
        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[self.code, self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            ft.Text("Part1:"),
            self.num1_p1,
            self.num2_p1,
            ft.Text("Part2:"),
            self.num1_p2,
            self.num2_p2,
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"code": self.code, "p1n1": self.num1_p1, "p1n2": self.num2_p1,
                   "p2n1": self.num1_p2, "p2n2": self.num2_p2})
        try:
            self.check()
        except AssertionError:
            pass
        else:
            res = self.test.process(*self.data.values())

            self.view.controls.clear()
            text = "\n".join(res)
            result_text = ft.Text(value=text, selectable=True, size=14)
            self.view.controls.append(result_text)

            self._page.update()

    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array(vals)

        assert eng.is_float(vals[1])
        assert eng.is_float(vals[2])
        assert eng.is_int(vals[3])
        assert eng.is_int(vals[4])

