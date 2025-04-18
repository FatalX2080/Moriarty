try:
    from test import Supportive
except ModuleNotFoundError:
    from .test import Supportive


class Task10(Supportive):
    def __init__(self):
        super().__init__()

    def __minus(self, x):
        return bin(int(''.join([str(int(not int(a))) for a in x]), 2) + 1)[2:].zfill(len(x))

    def __sum(self, x, y):
        z = bin(int(x, 2) + int(y, 2))[2:]
        return z[-len(x):], z[:-len(x)]

    def __shift_left(self, x, y):
        return x[y:] + '0' * y

    def __bitnot(self, x):
        return str(int(not int(x)))

    def __division1(self, x, y):
        sign = str(int(x[0]) ^ int(y[0]))
        self.print('Знак =', sign)
        z = sign + '.'
        x = '0' + x[1:]
        y = '0' + y[1:]
        self.print('x =', x)
        self.print('y =', y)
        my = self.__minus(y)
        self.print('-y =', my)
        a, _ = self.__sum(x, my)
        self.print(f'\n   {x}\n + {my}\n   -----\na0={a}')
        for i in range(1, len(x)):
            self.print(f'a{i - 1} {">=" if a[0] == '0' else "<"} 0')
            a = self.__shift_left(a, 1)
            self.print(f'2a{i - 1} = {a}')
            self.print()
            if a[0] == '0':  # a >= 0
                self.print(f'   {a} = 2a{i - 1}\n + {my} = -Y\n   -----')
                a, _ = self.__sum(a, my)
            else:  # a < 0
                self.print(f'   {a} = 2a{i - 1}\n + {y} = Y\n   -----')
                a, _ = self.__sum(a, y)
            self.print(f'a{i}={a}')
            self.print(f' z{i} = {self.__bitnot(a[0])}')
            z += self.__bitnot(a[0])
        self.print('-' * 30)
        return z

    def __division2(self, x, y):
        self.print('x =', x)
        self.print('y =', y)
        sx = x[0]
        self.print('Знак X =', x[0])
        sy = y[0]
        self.print('Знак Y =', sy)
        z = ''
        my = self.__minus(y)
        self.print('-y =', my)
        if sx == sy:
            self.print('Зx = Зy')
            self.print()
            self.print(f'   {x} = x\n + {my} = -Y\n   -----')
            a, _ = self.__sum(x, my)
        else:
            self.print('Зx != Зy')
            self.print()
            self.print(f'   {x} = x\n + {y} = Y\n   -----')
            a, _ = self.__sum(x, y)
        self.print(f'a0={a}')

        for i in range(1, len(x) + 1):
            sa = a[0]
            a = self.__shift_left(a, 1)
            if sa == sy:
                self.print(f'Зa = Зy, z{i - 1} = 1')
                z += '1'

                self.print(f'2a{i - 1} = {a}')
                self.print()
                self.print(f'   {a} = 2a{i - 1}\n + {my} = -Y\n   -----')
                a, _ = self.__sum(a, my)
            else:
                self.print(f'Зa != Зy, z{i - 1} = 0')
                z += '0'
                self.print(f'2a{i - 1} = {a}')
                self.print()
                self.print(f'   {a} = 2a{i - 1}\n + {y} = Y\n   -----')
                a, _ = self.__sum(a, y)
            self.print(f'a{i}={a}')
        return z

    def process(self, a: str, b: str, code: str) -> list:
        """
        :param a: Operand 1
        :param b: Operand 2
        :param code: char - (p/d)
        :return: logs
        """
        self.reset_logs()
        a = a.replace(".", "")
        b = b.replace(".", "")
        res = self.__division1(a, b)
        text = '\nДеление в ПК: z = {0}' if code == "p" else '\nДеление в ДК: z ={0}'
        self.print()
        self.print(text.format(res))
        return self.get_logs()


if __name__ == '__main__':
    task = Task10()
    print("\n".join(task.process('0.1011', '0.1011', "p")))
    print("\n".join(task.process('0.1011', '0.1011', "d")))
