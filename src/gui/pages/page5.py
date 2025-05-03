import flet as ft
import flet.canvas as cv
from tests import Task5v1, Task5v2

from .base import TaskBasePage, TableDraftsman, AdjacencyTableDraftsman, BasicChecks


class Page5(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 5
        self.data = {}
        self.testV1 = Task5v1()
        self.testV2 = Task5v2()
        self.draftsman = TableDraftsman()
        self.adj_draftsman = AdjacencyTableDraftsman()

        self.count = ft.TextField(label="Count of variables")
        self.res = ft.TextField(label="Results f(x)")

        self.version = ft.Dropdown(
            label="Version", autofocus=True, value="v2",
            options=[ft.dropdown.Option("v2"), ft.dropdown.Option("v1")]
        )
        self.function = ft.Dropdown(
            label="func", autofocus=True, value="MDNF",
            options=[ft.dropdown.Option("MDNF"), ft.dropdown.Option("MKNF")]
        )

        self.canvas = cv.Canvas(width=self.win_size[0] * 0.93, height=self.win_size[0] * 0.93)
        self.function_text = ft.Text("M(D/K)NF", weight=ft.FontWeight.BOLD)
        self.icon = ft.Icon(name=ft.icons.ACCESS_TIME, color=ft.Colors.WHITE)
        self.adj_table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(""))],
            column_spacing=5, horizontal_margin=5
        )

        self.version.on_change = self.call_alert
        self._page = self.pinit()

    def call_alert(self, e):
        if self.version.value == "v1":
            alert = self.dinit()
            e.control.page.overlay.append(alert)
            alert.open = True
        else:
            self.evaluate_btn.disabled = False

        e.page.update()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        adj_table = ft.Row(
            controls=[self.adj_table],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            wrap=False
        )

        function_row = ft.Row(controls=[self.icon, self.function_text], scroll=ft.ScrollMode.AUTO)

        answers_list = ft.ListView(
            height=self.win_size[1] * 0.55,
            spacing=10,
            controls=[self.canvas, adj_table, function_row],
        )

        task_content = [
            self.count,
            self.res,
            ft.Row([self.version, self.function]),
            ft.Divider(height=1),
            res_row,
            answers_list
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    def dinit(self):
        cupertino_alert_dialog = None
        warning_text = "Attention!!! This version of the solver was written by one person and is still" \
                       " in the RAW ALPHA version. By clicking OK, you agree that its creator is not" \
                       " responsible for the correctness of the answers."

        def accept_dialog(e):
            self.evaluate_btn.disabled = False
            cupertino_alert_dialog.open = False
            e.control.page.update()

        def close_dialog(e):
            self.evaluate_btn.disabled = True
            cupertino_alert_dialog.open = False
            e.control.page.update()

        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Disclaimer of liability"),
            content=ft.Text(warning_text),
            actions=[
                ft.CupertinoDialogAction("OK", is_destructive_action=True, on_click=accept_dialog),
                ft.CupertinoDialogAction(text="Cancel", on_click=close_dialog),
            ],
        )
        return cupertino_alert_dialog

        # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"count": self.count, "res": self.res, "func": self.function})
        try:
            self.check()
        except AssertionError:
            self.open_error_dialogue(e)
            return

        try:
            # process
            if not self.data["func"]:
                func = self.testV2
            else:
                func = self.testV2 if self.version.value == "v2" else self.testV1
            cubes, t_data, sdknf, confirmed = func.process(*self.data.values())

            # canvas
            self.draftsman.set_atr(self.data["res"], cubes, self.win_size)
            self.canvas.clean()
            self.canvas.shapes = self.draftsman.draw(str(self.data["func"]))

            # answer
            func_name = "MDNF" if self.data["func"] else "MKNF"
            self.function_text.value = "{0} {1}".format(func_name, sdknf)
            self.icon.name = ft.Icons.CHECK if confirmed else ft.Icons.CLOSE

            # table
            col, rows = self.adj_draftsman.draw(*t_data)
            self.adj_table.columns = col
            self.adj_table.rows = rows

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
        borders = (0, 2 ** int(vals[0]) - 1)
        fv = [int(el) for el in vals[1].split()]
        assert eng.borders(max(fv), borders)
        assert eng.borders(min(fv), borders)

        self.data["count"] = int(self.data["count"])
        self.data["func"] = int(self.data["func"] == "MDNF")
        self.data["res"] = list(sorted(self.data["res"].split()))
