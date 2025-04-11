import flet as ft
import flet.canvas as cv
from .base import TaskBasePage
from tests import Task7


class Page7(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 7
        self.data = {}
        self.test = Task7()

        self.num = ft.TextField(label="Number")
        self.np = ft.TextField(label="n(п)")
        self.nm = ft.TextField(label="n(m)")

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
            self.num,
            self.np,
            self.nm,
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"number": self.num, "p": self.np, "m": self.nm})
        assert self.check()
        self.data["p"] = int(self.data["p"])
        self.data["m"] = int(self.data["m"])
        res = self.test.process(*self.data.values())

        self.view.controls.clear()
        result_text = ft.Text(
            value="\n".join(res),
            selectable=True,
            size=14,
        )
        self.view.controls.append(result_text)

        self._page.update()
