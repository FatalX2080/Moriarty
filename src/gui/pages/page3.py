import flet as ft
from .base import TaskBasePage

from tests import Task3

class Page3(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 3
        self.data = {}
        self.test = Task3()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.SDNF_text = ft.Text("SDNF", weight=ft.FontWeight.BOLD)
        self.SKNF_text = ft.Text("SKNF", weight=ft.FontWeight.BOLD)

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

