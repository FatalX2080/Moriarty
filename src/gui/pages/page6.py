import flet as ft
import flet.canvas as cv
from tests import Task6

from .base import TaskBasePage, TableDraftsman, AdjacencyTableDraftsman, BasicChecks


class Page6(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 6
        self.data = {}
        self.test = Task6()
        self.adj_draftsman = AdjacencyTableDraftsman()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")
        self.fres = ft.TextField(label="Forbidden results")

        canv_size = self.win_size[0] * 0.93
        self.mdnf_canvas = cv.Canvas(width=canv_size, height=canv_size)
        self.mknf_canvas = cv.Canvas(width=canv_size, height=canv_size)

        self.mdnf_text = ft.Text("MDNF", weight=ft.FontWeight.BOLD)
        self.mknf_text = ft.Text("MKNF", weight=ft.FontWeight.BOLD)

        self.mdnf_adj_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(""))],
            column_spacing=5, horizontal_margin=5
        )
        self.mknf_adj_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(""))],
            column_spacing=5, horizontal_margin=5
        )

        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        d_adj_table = ft.Row(
            controls=[self.mdnf_adj_table],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            wrap=False
        )

        k_adj_table = ft.Row(
            controls=[self.mdnf_adj_table],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            wrap=False
        )

        mdnf_function_row = ft.Row(controls=[self.mdnf_text], scroll=ft.ScrollMode.AUTO)
        mknf_function_row = ft.Row(controls=[self.mknf_text], scroll=ft.ScrollMode.AUTO)

        answers_list = ft.ListView(
            height=self.win_size[1] * 0.5,
            spacing=10,
            controls=[
                ft.Text("MDNF", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.mdnf_canvas,
                d_adj_table,
                mdnf_function_row,
                ft.Divider(height=2),
                ft.Text("MKNF", style=ft.TextThemeStyle.DISPLAY_SMALL),
                self.mknf_canvas,
                k_adj_table,
                mknf_function_row,
            ],
        )

        task_content = [
            self.count,
            self.res,
            self.fres,
            ft.Divider(height=2),
            res_row,
            answers_list
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    def process(self, e):
        self.read({"count": self.count, "res": self.res, "fres": self.fres})

        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
            return

        try:
            # process
            mDnf, mKnf = self.test.process(*self.data.values())

            Dcubes, Dt_data, Dmnf, _ = mDnf
            Kcubes, Kt_data, Kmnf, _ = mKnf

            # canvas
            dvals = self.data["res"] + self.data["fres"]
            kvals = self.test.gen_knf(self.data["res"])

            draftsman = TableDraftsman()
            draftsman.set_atr(dvals, Dcubes, self.win_size)
            self.mdnf_canvas.clean()
            self.mdnf_canvas.shapes = draftsman.draw("1")

            draftsman = TableDraftsman()
            draftsman.set_atr(tuple(kvals), Kcubes, self.win_size)
            self.mknf_canvas.clean()
            self.mknf_canvas.shapes = draftsman.draw("0")

            # answer
            self.mdnf_text.value = "MDNF {0}".format(Dmnf)
            self.mknf_text.value = "MKNF {0}".format(Kmnf)

            # table
            col, rows = self.adj_draftsman.draw(*Dt_data)
            self.mdnf_adj_table.columns = col
            self.mdnf_adj_table.rows = rows

            col, rows = self.adj_draftsman.draw(*Kt_data)
            self.mknf_adj_table.columns = col
            self.mknf_adj_table.rows = rows

            self._page.update()
        except:
            self.open_text_error_dialogue(e)


    def check(self):
        vals = list(self.data.values())
        eng = BasicChecks()

        assert eng.void_array(vals)

        assert eng.is_int(vals[0])
        assert eng.borders(vals[0], (4, 4))

        borders = (1, 2 ** int(vals[0]))
        assert eng.borders(len(vals[1].split()), borders)
        assert eng.borders(len(vals[2].split()), borders)

        borders = (0, 2 ** int(vals[0]) - 1)
        fv = [int(el) for el in vals[1].split()]
        assert eng.borders(max(fv), borders)
        assert eng.borders(min(fv), borders)
        borders = (0, 2 ** int(vals[0]) - 1)
        fv = [int(el) for el in vals[2].split()]
        assert eng.borders(max(fv), borders)
        assert eng.borders(min(fv), borders)

        self.data["count"] = int(self.data["count"])
        self.data["res"] = list(sorted(self.data["res"].split()))
        self.data["fres"] = list(sorted(self.data["fres"].split()))
