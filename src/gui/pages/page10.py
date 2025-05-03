import flet as ft
from tests import Task10

from .base import TaskBasePage, BasicChecks


class Page10(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 10
        self.data = {}
        self.test = Task10()

        self.num1p = ft.TextField(label="Operand 1")
        self.num2p = ft.TextField(label="Operand 2")

        self.num1d = ft.TextField(label="Operand 1")
        self.num2d = ft.TextField(label="Operand 2")

        self.view = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=self.win_size[0],
            height=self.win_size[1] * 0.38,
            spacing=10,
        )
        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            ft.Text("PK:"),
            self.num1p,
            self.num2p,
            ft.Text("DK:"),
            self.num1d,
            self.num2d,
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"1p": self.num1p, "2p": self.num2p, "1d": self.num1d, "2d": self.num2d})
        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
            return

        try:
            pack1 = [self.data["1p"], self.data["2p"], "p"]
            resp = self.test.process(*pack1)
            pack2 = [self.data["1d"], self.data["2d"], "d"]
            resd = self.test.process(*pack2)

            self.view.controls.clear()
            text = "\n".join(resp) + "\n" * 8 + "\n".join(resd)
            result_text = ft.Text(value=text, selectable=True, size=14)
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
        assert eng.is_float(vals[2])
        assert eng.is_float(vals[3])
