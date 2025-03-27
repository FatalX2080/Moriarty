import flet as ft
import tests

class BasePage:
    def __init__(self):
        self._page = None

        nav = ft.NavigationDrawerDestination
        navigate_list = [nav(label="Home", icon=ft.Icons.HOME)]
        nv_list = navigate_list + [nav(label="Test {0}".format(index)) for index in range(1, 14)]
        self.navigation = ft.NavigationDrawer(controls=nv_list)

    def open_navigate(self, e):
        e.control.page.drawer = self.navigation
        self.navigation.open = True
        e.control.page.update()

    def set_switch_event(self, switch_func):
        self.navigation.on_change = switch_func


# ----------------------------------------------------------------------------------------------------------
class Page0(BasePage):
    def __init__(self):
        super().__init__()
        self._page = self.pinit()

    def render(self, g):
        g().alignment = ft.alignment.center
        g().content = self._page

    def pinit(self):
        return ft.Column([
            ft.ElevatedButton("Open end drawer", on_click=self.open_navigate),
        ])


class Page1(BasePage):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.test = tests.Task1()

        self.sign = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value="+", label="+"),
                    ft.Radio(value="-", label="-"),
                    ft.Radio(value="*", label="*"),
                    ft.Radio(value="/", label="/"),
                ]
            ), value="+"
        )
        self.val1_field = ft.TextField(label="Num 1")
        self.val2_field = ft.TextField(label="Num 2")
        self.base_field = ft.TextField(label="Base")
        self.res_text = ft.Text("Result")

        self._page = self.pinit()

    def pinit(self):
        return ft.Column([
            ft.Text("Test 1", theme_style=ft.TextThemeStyle.DISPLAY_LARGE),
            self.val1_field,
            self.val2_field,
            self.base_field,
            ft.Text("Operation"),
            self.sign,
            self.res_text,
            ft.Button(text="Evaluate", on_click=self.process),
            ft.Button(text="Home", icon=ft.icons.HOME, on_click=self.open_navigate),
        ])

    def render(self, g):
        g().content = self._page

    # ------------------------------------------------------------------------------------------------------
    def process(self, e):
        self.read()
        assert self.check()
        self.data["base"] = int(self.data["base"])
        res = self.test.process(self.data["op"], self.data["values"], self.data["base"])
        # TODO Старый текст не очищается
        self.res_text.value = "Result: {0}".format(res)
        self._page.update()

    def read(self):
        self.data["op"] = self.sign.value
        self.data["values"] = (self.val1_field.value, self.val2_field.value)
        self.data["base"] = self.base_field.value

    def check(self) -> bool:
        try:
            if self.data["values"][0] == "":
                return False
            if self.data["values"][1] == "":
                return False
            if self.data["base"] == "":
                return False
            int(self.data["values"][0])
            int(self.data["values"][1])
            int(self.data["base"])
        except ValueError:
            return False
        return True
