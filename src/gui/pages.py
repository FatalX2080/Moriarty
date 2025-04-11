import flet as ft
import flet.canvas as cv
from .navigate import BottomBar
import tests


class BasePage:
    win = None
    win_size = None
    page_list = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        bar = BottomBar(BasePage.win, BasePage.page_list)
        self.bottom_bar = bar.NavBar
        self._page = None
        self.win = BasePage.win

    def render(self):
        BasePage.win.content = self._page


class TaskBasePage(BasePage):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self.index = 0
        self.data = {}
        self.evaluate_btn = ft.Button(text="Evaluate", on_click=self.process)

    def process(self, e):
        pass

    def join_top(self, task_block) -> ft.Container:
        col = ft.Column
        cont = ft.Container

        title = cont(
            content=ft.Text(
                "Test {0}".format(self.index),
                theme_style=ft.TextThemeStyle.DISPLAY_LARGE
            ),
            alignment=ft.alignment.center,
            expand=True,
        )
        return cont(col([title, cont(col(task_block))]))

    def join_page(self, top_part):
        return ft.Container(
            content=ft.Column(
                controls=[top_part, self.bottom_bar],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            expand=True
        )

    def read(self, entries: dict):
        self.data.clear()
        for k in entries.keys(): self.data[k] = entries[k].value

    def check(self):
        return True


class TableDraftsman:
    addressing = {
        "0": (3, 3),
        "1": (3, 2),
        "2": (2, 3),
        "3": (2, 2),

        "4": (3, 0),
        "5": (3, 1),
        "6": (2, 0),
        "7": (2, 1),

        "8": (0, 3),
        "9": (0, 2),
        "10": (1, 3),
        "11": (1, 2),

        "12": (0, 0),
        "13": (0, 1),
        "14": (1, 0),
        "15": (1, 1),
    }

    def __init__(self):
        self.fields = None
        self.cubes = None
        self.win_size = None

        self.cell_size = 0

        self.base_color = ft.colors.WHITE
        self.base = []

    def set_atr(self, fields, cubes, win_size):
        self.fields = fields
        self.cubes = cubes
        self.win_size = win_size

    def calculate_sizes(self):
        self.cell_size = self.win_size[0] * 0.93 // 4
        table_size = self.cell_size * 4

        return (self.cell_size, self.cell_size), (table_size, table_size)

    def gen_colors(self):
        from random import shuffle
        colors = [ft.colors.RED, ft.colors.GREEN, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PINK,
                  ft.colors.PURPLE, ft.colors.ORANGE, ft.colors.CYAN]
        shuffle(colors)
        return colors[:len(self.cubes)]

    def draw_table(self):
        stroke_paint = ft.Paint(color=self.base_color, stroke_width=2, style=ft.PaintingStyle.STROKE)

        cell_size, table_size = self.calculate_sizes()
        cells = [cv.Rect(self.cell_size * i, self.cell_size * j, *cell_size, paint=stroke_paint)
                 for i in range(4) for j in range(4)]

        self.base += cells

    def draw_digits(self, digit="1"):
        digits = []
        t_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=46, color=self.base_color)

        for cell in self.fields:
            cords = TableDraftsman.addressing[cell]
            cords = ((cords[1] + 0.35) * self.cell_size, (cords[0] + 0.2) * self.cell_size)
            digits.append(cv.Text(*cords, text=digit, style=t_style))

        self.base += digits

    def draw_cubes(self):
        cubes = []
        colors = self.gen_colors()
        rec = ft.Paint(color=ft.colors.BLACK, stroke_width=2, style=ft.PaintingStyle.STROKE)
        for iex, cube in enumerate(self.cubes):
            rec.color = colors[iex]
            start = ((cube[1] + 0.15) * self.cell_size, (cube[0] + 0.15) * self.cell_size)
            size = ((cube[2][1] - 0.3) * self.cell_size, (cube[2][0] - 0.3) * self.cell_size)
            cb = cv.Rect(*start, *size, paint=rec)
            cubes.append(cb)

        self.base += cubes

    def draw(self) -> list:
        # TODO пока неверно отрисовывает разделённые кубы
        self.draw_table()
        self.draw_digits()
        self.draw_cubes()
        return self.base


# ----------------------------------------------------------------------------------------------------------

class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self._page = self.pinit()

    def pinit(self):
        return ft.Column(
            controls=[ft.Text("Template"), self.bottom_bar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


# ----------------------------------------------------------------------------------------------------------


class Page1(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 1
        self.test = tests.Task1()

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
        assert self.check()
        self.data["base"] = int(self.data["base"])
        res = self.test.process(self.data["op"], (self.data["v1"], self.data["v2"]), self.data["base"])
        self.res_text.value = "Result {0}".format(res)
        self._page.update()


class Page2(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 2
        self.data = {}
        self.test = tests.Task2()

        self.num = ft.TextField(label="Number")
        self.baseX = ft.TextField(label="Base x")
        self.baseAns = ft.TextField(label="Base ans")
        self.lgX = ft.TextField(label="Lg x")
        self.lgAns = ft.TextField(label="Lg ans")

        self.len_text = ft.Text("Fract len", weight=ft.FontWeight.BOLD)
        self.res_text = ft.Text("Result", weight=ft.FontWeight.BOLD)
        self.res_text.spans.append(ft.TextSpan(style=ft.TextStyle(size=9)))

        self._page = self.pinit()

    def pinit(self):
        row = ft.Row
        res_row = row(
            controls=[self.len_text, self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        task_content = [
            self.num,
            self.baseX,
            self.baseAns,
            self.lgX,
            self.lgAns,
            ft.Divider(height=1),
            res_row,
            self.res_text
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({
            "x": self.num, "base_x": self.baseX, "base_ans": self.baseAns,
            "lg_x": self.lgX, "lg_ans": self.lgAns
        })
        assert self.check()
        self.data["base_x"] = int(self.data["base_x"])
        self.data["base_ans"] = int(self.data["base_ans"])
        self.data["lg_x"] = float(self.data["lg_x"])
        self.data["lg_ans"] = float(self.data["lg_ans"])
        res = self.test.process(*self.data.values())
        self.len_text.value = "Fract len {0} -> {1}".format(res[0], res[1])
        self.res_text.value = "Result {0}".format(res[3][0])
        self.res_text.spans[0].text = "{0}".format(res[2])
        self._page.update()


class Page3(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 3
        self.data = {}
        self.test = tests.Task3()

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


class Page4(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 4
        self.data = {}
        self.test = tests.Task4()

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


class Page5(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 5
        self.data = {}
        self.test = tests.Task5()
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


class Page7(TaskBasePage):
    def __init__(self):
        super().__init__()
        self.index = 7
        self.data = {}
        self.test = tests.Task7()

        self.num = ft.TextField(label="Number")
        self.np = ft.TextField(label="n(п)")
        self.nm = ft.TextField(label="n(m)")

        self.view = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            width=self.win_size[0],
            height=self.win_size[1] * 0.5,
            spacing=10,
        )
        self._page = self.pinit()

    def pinit(self):
        res_row = ft.Row(
            controls=[ft.Text(""), self.evaluate_btn],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        task_content = [
            self.num,
            self.np,
            self.nm,
            ft.Divider(height=1),
            res_row,
            self.view,
        ]
        top_part = self.join_top(task_content)
        return self.join_page(top_part)

    # ------------------------------------------------------------------------------------------------------

    def process(self, e):
        self.read({"number": self.num, "p": self.np, "m": self.nm})
        assert self.check()
        self.data["p"] = int(self.data["p"])
        self.data["m"] = int(self.data["m"])
        res = self.test.process(*self.data.values())

        self.view.controls.clear()
        result_text = ft.Text(
            value="\n".join(res),
            selectable=True,
            size=14,
        )
        self.view.controls.append(result_text)

        self._page.update()
