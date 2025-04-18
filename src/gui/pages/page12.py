import flet as ft
from tests import Task12

from .base import TaskBasePage


class Page12(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 12
        self.data = {}
        self.test = Task12()

        self.num1 = ft.TextField(label="Operand 1")
        self.num2 = ft.TextField(label="Operand 2")

        self.operation = ft.Dropdown(
            label="code", autofocus=True, value="-",
            options=[ft.dropdown.Option("+"), ft.dropdown.Option("-")],
        )

        self.view = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=self.win_size[0],
            height=self.win_size[1] * 0.55,
            spacing=10,
        )
        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[self.operation, self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.num1,
            self.num2,
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"op":self.operation, "1p": self.num1, "2p": self.num2})
        assert self.check()

        res = self.test.process(*self.data.values())

        self.view.controls.clear()
        result_text = ft.Text(value="\n".join(res), selectable=True, size=14)
        self.view.controls.append(result_text)

        self._page.update()
