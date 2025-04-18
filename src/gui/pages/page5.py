import flet as ft
import flet.canvas as cv
from .base import TaskBasePage, TableDraftsman, AdjacencyTableDraftsman
from tests import Task5v1, Task5v2


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

        # TODO заменить на Chip
        self.silent_checker = ft.Checkbox(label="Silene check", value=True)
        self.version = ft.Dropdown(
            label="Version", autofocus=True, value="v2",
            options=[ft.dropdown.Option("v2"), ft.dropdown.Option("v1")]
        )

        self.canvas = cv.Canvas(width=self.win_size[0] * 0.93, height=self.win_size[0] * 0.93)
        self.function_text = ft.Text("SDNF", weight=ft.FontWeight.BOLD)
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
            controls=[self.silent_checker, self.version, self.evaluate_btn],
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
        self.read({"count": self.count, "res": self.res, "sch": self.silent_checker})

        assert self.check()

        self.data["count"] = int(self.data["count"])
        self.data["res"] = list(sorted(self.data["res"].split()))
        self.data["sch"] = bool(self.data["sch"])

        # process
        func = self.testV2 if self.version.value == "v2" else self.testV1
        cubes, t_data, sdnf, confirmed = func.process(*self.data.values())

        # canvas
        self.draftsman.set_atr(self.data["res"], cubes, self.win_size)
        self.canvas.clean()
        self.canvas.shapes = self.draftsman.draw()

        # answer
        self.function_text.value = "SDNF {0}".format(sdnf)
        if self.data["sch"]:
            self.icon.name = ft.Icons.CHECK if confirmed else ft.Icons.CLOSE
        else:
            self.icon.name = ft.Icons.QUESTION_MARK

        # table
        col, rows = self.adj_draftsman.draw(*t_data)
        self.adj_table.columns = col
        self.adj_table.rows = rows

        self._page.update()
