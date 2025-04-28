import flet as ft
import flet.canvas as cv
from tests.test5 import addressing

from ..navigate import BottomBar


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
        self.bottom_bar = BottomBar(BasePage.win, BasePage.page_list)
        self._page = None
        self.alert = None
        self.win = BasePage.win
        self.index = 0

    def render(self, event=None):
        if self.alert is not None:
            event.control.page.overlay.append(self.alert)
            self.alert.open = True
        self.bottom_bar.set_page_index(self.index)
        BasePage.win.content = self._page

    def pinit(self):
        return None


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
                controls=[top_part, self.bottom_bar.NavBar],
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

    def __init__(self):
        self.fields = None
        self.cubes = None
        self.win_size = None

        self.cell_size = 0

        self.base_color = ft.colors.WHITE
        self.base = []

    def set_atr(self, fields: tuple | list, cubes: tuple | list, win_size: tuple | list):
        self.fields = list(fields)
        self.fields.sort()
        self.cubes = cubes
        self.win_size = win_size

    def calculate_sizes(self):
        self.cell_size = self.win_size[0] * 0.93 // 4
        table_size = self.cell_size * 4

        return (self.cell_size, self.cell_size), (table_size, table_size)

    def gen_colors(self):
        from random import shuffle
        colors = [ft.colors.RED, ft.colors.GREEN, ft.colors.BLUE, ft.colors.YELLOW, ft.colors.PINK,
                  ft.colors.PURPLE, ft.colors.ORANGE, ft.colors.CYAN, ft.colors.GREY, ft.colors.TEAL,
                  ft.colors.LIME, ft.colors.BROWN]
        shuffle(colors)
        return colors[:len(self.cubes)]

    def draw_table(self):
        stroke_paint = ft.Paint(color=self.base_color, stroke_width=2, style=ft.PaintingStyle.STROKE)

        cell_size, table_size = self.calculate_sizes()
        cells = [cv.Rect(self.cell_size * i, self.cell_size * j, *cell_size, paint=stroke_paint)
                 for i in range(4) for j in range(4)]

        self.base += cells

    def draw_digits(self, digit="1", show_numerating=False):
        digits = []
        t_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=46, color=self.base_color)
        info_style = ft.TextStyle(weight=ft.FontWeight.BOLD, size=13, color=self.base_color)

        for num in range(16):
            cords = addressing[str(num)]
            if show_numerating:
                text_cords = ((cords[1] + 0.76) * self.cell_size, (cords[0] + 0.75) * self.cell_size)
                digits.append(cv.Text(*text_cords, text=str(num), style=info_style))
            if str(num) in self.fields:
                text_cords = ((cords[1] + 0.35) * self.cell_size, (cords[0] + 0.2) * self.cell_size)
                digits.append(cv.Text(*text_cords, text=digit, style=t_style))

        self.base += digits

    def draw_cube(self, cube, color) -> list:
        OFFSET = 0.15
        paint = ft.Paint(color=color, stroke_width=2, style=ft.PaintingStyle.STROKE)
        line = cv.Line
        """
        @ @ @ @ 0 0
        @ @ @ @ 0 0
        @ @ @ @ 0 0
        @ @ @ @ 0 0
        0 0 0 0 0 0
        0 0 0 0 0 0
        """
        x0 = cube[1]
        y0 = cube[0]

        x1 = x0 + cube[2][1]
        y1 = y0 + cube[2][0]

        lines = []
        if x1 <= 4 and y1 <= 4:
            coords = [
                [(x0 + OFFSET), (y0 + OFFSET), (x1 - OFFSET), (y0 + OFFSET)],  # -
                [(x0 + OFFSET), (y0 + OFFSET), (x0 + OFFSET), (y1 - OFFSET)],  # |
                [(x1 - OFFSET), (y0 + OFFSET), (x1 - OFFSET), (y1 - OFFSET)],  # |
                [(x0 + OFFSET), (y1 - OFFSET), (x1 - OFFSET), (y1 - OFFSET)]  # _
            ]
        elif x1 > 4 and y1 <= 4:
            coords = [
                [(x0 + OFFSET), (y0 + OFFSET), 4, (y0 + OFFSET)],
                [(x0 + OFFSET), (y0 + OFFSET), (x0 + OFFSET), (y1 - OFFSET)],
                [(x0 + OFFSET), (y1 - OFFSET), 4, (y1 - OFFSET)],

                [0, (y0 + OFFSET), (x1 - 4 - OFFSET), (y0 + OFFSET)],
                [(x1 - 4 - OFFSET), (y0 + OFFSET), (x1 - 4 - OFFSET), (y1 - OFFSET)],
                [0, (y1 - OFFSET), (x1 - 4 - OFFSET), (y1 - OFFSET)]
            ]
        elif x1 <= 4 and y1 > 4:
            coords = [
                [(x0 + OFFSET), (y0 + OFFSET), (x1 - OFFSET), (y0 + OFFSET)],
                [(x0 + OFFSET), (y0 + OFFSET), (x0 + OFFSET), 4],
                [(x1 - OFFSET), (y0 + OFFSET), (x1 - OFFSET), 4],

                [(x0 + OFFSET), (y1 - 4 - OFFSET), (x1 - OFFSET), (y1 - 4 - OFFSET)],
                [(x0 + OFFSET), 0, (x0 + OFFSET), (y1 - 4 - OFFSET)],
                [(x1 - OFFSET), 0, (x1 - OFFSET), (y1 - 4 - OFFSET)]
            ]
        else:
            coords = [
                [(x0 + OFFSET), (y0 + OFFSET), 4, (y0 + OFFSET)],
                [(x0 + OFFSET), (y0 + OFFSET), (x0 + OFFSET), 4],

                [0, (y0 + OFFSET), (x1 - 4 - OFFSET), (y0 + OFFSET)],
                [(x1 - 4 - OFFSET), (y0 + OFFSET), (x1 - 4 - OFFSET), 4],

                [(x0 + OFFSET), (y1 - 4 - OFFSET), 4, (y1 - 4 - OFFSET)],
                [(x0 + OFFSET), 0, (x0 + OFFSET), (y1 - 4 - OFFSET)],

                [0, (y1 - 4 - OFFSET), (x1 - 4 - OFFSET), (y1 - 4 - OFFSET)],
                [(x1 - 4 - OFFSET), 0, (x1 - 4 - OFFSET), (y1 - 4 - OFFSET)]
            ]

        for c in coords: lines.append(line(*[cord * self.cell_size for cord in c], paint=paint))

        return lines

    def draw_cubes(self):
        cubes = []
        colors = self.gen_colors()
        for iex, cube in enumerate(self.cubes):
            p_obj = self.draw_cube(cube, colors[iex])
            cubes += p_obj
        self.base += cubes

    def draw(self, digit) -> list:
        self.draw_table()
        self.draw_digits(digit)
        self.draw_cubes()
        return self.base


class AdjacencyTableDraftsman:
    def __init__(self):
        pass

    def draw(self, rows, cols, table):
        base_col = [ft.DataColumn(ft.Text(""))]
        base_col += [
            ft.DataColumn(ft.Text(text, weight=ft.FontWeight.BOLD)) for text in cols
        ]

        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(rows[i], weight=ft.FontWeight.BOLD)),
                    *[
                        ft.DataCell(ft.Text(str(table[i][j]), italic=True))
                        for j in range(len(cols))
                    ]
                ],
            ) for i in range(len(rows))
        ]
        return base_col, rows
