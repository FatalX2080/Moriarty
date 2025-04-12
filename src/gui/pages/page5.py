import flet as ft
import flet.canvas as cv
from .base import TaskBasePage, TableDraftsman, AdjacencyTableDraftsman
from tests import Task5


# TODO доделать отказ от ответственности

class Page5(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 5
        self.data = {}
        self.test = Task5()
        self.draftsman = TableDraftsman()
        self.adj_draftsman = AdjacencyTableDraftsman()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.canvas = cv.Canvas(width=200, height=200)
        self.SDNF_text = ft.Text("SDNF", weight=ft.FontWeight.BOLD)
        self.adj_table = ft.DataTable(columns=[ft.DataColumn(ft.Text(""))], column_spacing=5,
                                      horizontal_margin=5
                                      )

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        view = ft.ListView(
            controls=[self.adj_table],

            auto_scroll=False,
            expand=True,
        )
        task_content = [
            self.count,
            self.res,
            ft.Divider(height=1),
            res_row,
            self.SDNF_text,
            ft.Container(
                ft.Column([
                    view,
                    self.canvas
                ]),
                scroll=ft.ScrollMode.AUTO,
            )
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"count": self.count, "res": self.res})
        assert self.check()
        self.data["count"] = int(self.data["count"])
        self.data["res"] = list(sorted(self.data["res"].split()))
        cubes, t_data, sdnf = self.test.process(*self.data.values())

        self.draftsman.set_atr(self.data["res"], cubes, self.win_size)
        self.canvas.clean()
        self.canvas.shapes = self.draftsman.draw()

        self.SDNF_text.value = "SDNF {0}".format(sdnf)

        col, rows = self.adj_draftsman.draw(*t_data)
        self.adj_table.columns = col
        self.adj_table.rows = rows

        self._page.update()
