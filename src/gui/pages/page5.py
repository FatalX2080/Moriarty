import flet as ft
import flet.canvas as cv
from .base import TaskBasePage, TableDraftsman
from tests import Task5


class Page5(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 5
        self.data = {}
        self.test = Task5()
        self.draftsman = TableDraftsman()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.canvas = cv.Canvas(width=200, height=200)

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.count,
            self.res,
            ft.Divider(height=1),
            res_row,
            self.canvas
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

        self.draftsman.set_atr(self.data["res"], res, self.win_size)
        self.canvas.clean()
        self.canvas.shapes = self.draftsman.draw()

        self._page.update()