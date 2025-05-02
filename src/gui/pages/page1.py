import flet as ft
from tests import Task1

from .base import TaskBasePage, BasicChecks


class Page1(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 1
        self.test = Task1()

        rbuttons = ft.Row(
            [
                ft.Container(
                    ft.Radio(value=opt, label=opt),
                    expand=True,
                    alignment=ft.alignment.center,
                )
                for opt in ["+", "-", "*", "//"]
            ],
            expand=True,
        )
        self.sign = ft.RadioGroup(content=rbuttons, value="+")
        self.val1_field = ft.TextField(label="Operand 1")
        self.val2_field = ft.TextField(label="Operand 2")
        self.base_field = ft.TextField(label="Base")
        self.res_text = ft.Text("Result", weight=ft.FontWeight.BOLD)

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[self.res_text, self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        task_content = [
            self.val1_field,
            self.val2_field,
            self.base_field,
            ft.Text("Operation"),
            self.sign,
            ft.Divider(height=1),
            res_row
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        rdict = {"op": self.sign, "v1": self.val1_field, "v2": self.val2_field, "base": self.base_field}
        self.read(rdict)
        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
        else:
            res = self.test.process(self.data["op"], (self.data["v1"], self.data["v2"]), self.data["base"])
            self.res_text.value = "Result {0}".format(res)
            self._page.update()

    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array([vals[1], vals[2], vals[3]])

        assert eng.is_int(vals[3])
        assert eng.borders(vals[3], (2, 16))

        assert eng.equal_length(vals[1], vals[2])

        assert eng.grounds(vals[1], int(vals[3]))
        assert eng.grounds(vals[2], int(vals[3]))

        self.data["base"] = int(self.data["base"])
