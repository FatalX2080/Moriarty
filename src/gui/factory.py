from .pages import Page0, Page1


class Factory:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, sw_event):
        self._pages_list = []

        self._pages_list.append(Page0())
        self._pages_list.append(Page1())

        self.base_config(sw_event)

    def base_config(self, sw_event):
        for page in self._pages_list:
            page.set_switch_event(sw_event)

    def get_list(self) -> list:
        return self._pages_list
