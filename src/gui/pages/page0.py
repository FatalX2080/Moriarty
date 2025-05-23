import flet as ft

from .base import BasePage
from ..descriptions import introduction, tech_info, test_info, wanted, git_link


class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self.index = 0
        self._page = self.pinit()

    def pinit(self):
        # Introduction -> test info -> project ->offer of cooperation
        w100 = ft.FontWeight.W_100
        ds = ft.TextThemeStyle.DISPLAY_SMALL

        page_title = ft.Container(
            content=ft.Text(
                "MORIARTY",
                theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM, weight=ft.FontWeight.W_300,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(bottom=20)
        )
        info_title = ft.Container(
            content=ft.Text("INFO", theme_style=ds, weight=w100),
            alignment=ft.alignment.center,
        )
        test_title = ft.Container(
            content=ft.Text("TEST", theme_style=ds, weight=w100),
            alignment=ft.alignment.center,
        )
        projest_title = ft.Container(
            content=ft.Text("PROJECT", theme_style=ds, weight=w100),
            alignment=ft.alignment.center,
        )
        last_title = ft.Container(
            content=ft.Text("WANTED", theme_style=ds, weight=w100),
            alignment=ft.alignment.center,
        )

        des = ft.GestureDetector(
            content=ft.Text(
                "git",
                size=16,
                color=ft.colors.BLUE,
                style=ft.TextStyle(ft.TextDecoration.UNDERLINE),
            ),
            on_tap=copy_link,
        )

        intro = ft.Column([ft.Text(introduction), ft.Row([ft.Text("Here is its:"), des])],
                          spacing=0)

        text_list = ft.ListView(
            height=self.win_size[1] * 0.89,
            spacing=10,
            controls=[
                page_title,
                ft.Divider(1),
                info_title,
                intro,
                ft.Divider(1),
                test_title,
                ft.Text(test_info),
                ft.Divider(1),
                projest_title,
                ft.Text(tech_info),
                ft.Divider(1),
                last_title,
                ft.Text(wanted)
            ]
        )

        return ft.Column(
            controls=[text_list, self.bottom_bar.NavBar],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


def copy_link(e):
    e.page.set_clipboard(git_link)
    dialog = ft.AlertDialog(
        title=ft.Text("Copied"),
        content=ft.Text(git_link),
        on_dismiss=lambda e: None,
    )

    e.control.page.overlay.append(dialog)
    dialog.open = True
    e.control.page.update()
