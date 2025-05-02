import flet as ft
from tests import Task4

from .base import TaskBasePage, BasicChecks


class Page4(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 4
        self.data = {}
        self.test = Task4()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.f_type = ft.Dropdown(
            label="function type", autofocus=True, value="1",
            options=[ft.dropdown.Option("1", "MDNF"), ft.dropdown.Option("0", "MKNF")],
        )

        self.MDNF_text = ft.Text("MDNF", weight=ft.FontWeight.BOLD)

        self._page = self.pinit()

    def pinit(self):
        function_row = ft.Row(controls=[self.MDNF_text], scroll=ft.ScrollMode.AUTO)

        res_row = ft.Row(
            controls=[self.f_type, self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.count,
            self.res,
            ft.Divider(height=1),
            res_row,
            function_row
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"count": self.count, "res": self.res, "f_type": self.f_type})
        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
            return

        try:
            res = self.test.process(*self.data.values())
            self.MDNF_text.value = "MDNF {0}".format(res)
            self._page.update()
        except:
            self.open_text_error_dialogue(e)

    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array(vals)

        assert eng.is_int(vals[0])
        assert eng.borders(vals[0], (1, 10))

        borders = (1, 2 ** int(vals[0]))
        assert eng.borders(len(vals[1].split()), borders)
        borders = (0, 2 ** int(vals[0]) - 1)
        fv = [int(el) for el in vals[1].split()]
        assert eng.borders(max(fv), borders)
        assert eng.borders(min(fv), borders)

        self.data["count"] = int(self.data["count"])
        self.data["res"] = list(sorted(self.data["res"].split()))
        self.data["f_type"] = int(self.data["f_type"])
