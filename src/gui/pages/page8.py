import flet as ft
from tests import Task8

from .base import TaskBasePage, BasicChecks


class Page8(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 8
        self.data = {}
        self.test = Task8()

        drop = ft.dropdown.Option

        self.input_code = ft.Dropdown(
            label="input code", autofocus=True, value="d",
            options=[drop("p"), drop("d"), drop("o")],
        )
        self.operation_code = ft.Dropdown(
            label="operation code", autofocus=True, value="mdk",
            options=[drop("mok"), drop("mdk")]
        )
        self.result_code = ft.Dropdown(
            label="result code", autofocus=True, value="p",
            options=[drop("p"), drop("d"), drop("o")],
        )
        self.operation = ft.Dropdown(
            label="func", autofocus=True, value="+",
            options=[drop("+"), drop("-")]
        )
        self.num1 = ft.TextField(label="Operand 1")
        self.num2 = ft.TextField(label="Operand 2")

        self.view = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=self.win_size[0],
            height=self.win_size[1] * 0.45,
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
            ft.Row(controls=[self.input_code, self.operation_code], expand=True),
            ft.Row(controls=[self.result_code, self.operation], expand=True),
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"input_code": self.input_code, "operation_code": self.operation_code,
                   "result_code": self.result_code, "operation": self.operation,
                   "num1": self.num1, "num2": self.num2})
        try:
            self.check()
        except AssertionError:
            return self.open_error_dialogue(e)

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

        assert eng.is_float(vals[4])
        assert eng.is_float(vals[5])
