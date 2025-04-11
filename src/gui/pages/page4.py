import flet as ft
from .base import TaskBasePage

from tests import Task4


class Page4(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 4
        self.data = {}
        self.test = Task4()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.SDNF_text = ft.Text("SDNF", weight=ft.FontWeight.BOLD)

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[self.SDNF_text, self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.count,
            self.res,
            ft.Divider(height=1),
            res_row
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"count": self.count, "res": self.res})
        assert self.check()
        self.data["count"] = int(self.data["count"])
        self.data["res"] = list(sorted(self.data["res"].split()))
        res = self.test.process(*self.data.values())
        self.SDNF_text.value = "SDNF {0}".format(res)

        self._page.update()


