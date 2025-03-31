class Supportive:
    def __init__(self):
        self.__logs = []

    def print(self, *args, end: str = '', sep: str = ' '):
        if args:
            text = sep.join(map(lambda x: str(x), args))
            self.__logs.append(text + end)
        else:
            self.__logs.append('')

    def get_logs(self):
        return self.__logs

    def reset(self):
        self.__logs = []
