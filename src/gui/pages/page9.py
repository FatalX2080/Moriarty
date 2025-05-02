import flet as ft
from tests import Task9

from .base import TaskBasePage, BasicChecks


class Page9(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 9
        self.data = {}
        self.test = Task9()

        drop = ft.dropdown.Option
        self.values_pass = ft.Dropdown(
            label="values pass", autofocus=True, value="o",
            options=[drop("o", "older"), drop("y", "younger")],
        )
        self.operation_code = ft.Dropdown(
            label="operation code", autofocus=True, value="d",
            options=[drop("p"), drop("d")]
        )
        self.num1 = ft.TextField(label="Operand 1")
        self.num2 = ft.TextField(label="Operand 2")

        self.view = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=self.win_size[0],
            height=self.win_size[1] * 0.5,
            spacing=10,
        )
        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.num1,
            self.num2,
            ft.Row(controls=[self.values_pass, self.operation_code], expand=True),
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"num1": self.num1, "num2": self.num2,
                   "values_pass": self.values_pass, "operation_code": self.operation_code})
        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
            return

        try:
            res = self.test.process(*self.data.values())

            self.view.controls.clear()
            result_text = ft.Text(value="\n".join(res), selectable=True, size=14)
            self.view.controls.append(result_text)

            self._page.update()
        except:
            self.open_text_error_dialogue(e)

    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array(vals)

        assert eng.is_float(vals[0])
        assert eng.is_float(vals[1])