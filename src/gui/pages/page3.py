import flet as ft
from tests import Task3

from .base import TaskBasePage, BasicChecks


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
        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
        else:
            res = self.test.process(*self.data.values())
            # TODO не влезает
            self.SDNF_text.value = "SDNF {0}".format(res[0])
            self.SKNF_text.value = "SKNF {0}".format(res[1])

        self._page.update()

    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array(vals)

        assert eng.is_int(vals[0])
        assert eng.borders(vals[0], (1, 10))

        assert eng.length(vals[1].split(), 2**int(vals[0]))
        assert eng.array_grounds(vals[1].split(), "0123456789"[:int(vals[0])])

        self.data["count"] = int(self.data["count"])
        self.data["res"] = tuple([int(r) for r in list(self.data["res"].split())])
