try:
    from test import Supportive, AuxiliaryFunctions
except ModuleNotFoundError:
    from .test import Supportive, AuxiliaryFunctions


class Task12(Supportive, AuxiliaryFunctions):  # By @Sarkoxed
    def __init__(self):
        super().__init__()

    def denormmin(self, x1, x2, y2):
        self.print('Необходима денормализация мантиссы, сместим ее на порядок вправо')
        x2, y2 = self.PinO(x2), self.PinO(y2)
        x2, y2 = x2[:2] + '0' + x2[2:], y2[:2] + '0' + y2[2:]
        x2, y2 = self.PinO(x2), self.PinO(y2)

        if x1 != ('0.' + '1' * (len(x1) - 2)):
            ed = '0.' + '0' * (len(x1) - 3) + '1'
            x1 = self.PinD(x1)
            ed = self.PinD(ed)
            x1 = self.plus(x1, ed)[2:]
            x1 = self.DinP(x1)
        else:
            x1 = '0.1' + '0' * (len(x1) - 2)

        self.print('Увеличенный порядок: ', x1)
        self.print('Мантисса первого в мoк: ', x2[0] + x2)
        self.print('Мантисса второго в мoк: ', y2[0] + y2)
        self.print(' ', x2[0] + x2)
        self.print('+')
        self.print(' ', y2[0] + y2)
        s = self.plus(x2, y2)
        self.print('-------------')
        self.print(' ', s)
        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)
        return [s[:-1], x1]

    def denormplu(self, x1, x2, y2):
        self.print('Необходима денормализация мантиссы, сместим ее на порядок влево')
        x2, y2 = self.PinO(x2), self.PinO(y2)
        x2, y2 = x2[:2] + x2[3:] + '0', y2[:2] + y2[3:] + '0'
        x2, y2 = self.PinO(x2), self.PinO(y2)
        if x1 != ('1.' + '1' * (len(x1) - 2)):
            # ed = '1.' + '0' * (len(x1) - 3) + '1'
            x1 = self.PinD(x1)
            # ed = self.PinD(ed)
            x1 = self.plus(x1, '1.' + '0' * (len(x1) - 3) + '1')[2:]
            x1 = self.DinP(x1)
        else:
            x1 = '1.1' + '0' * (len(x1) - 2)

        self.print('Уменьшенный порядок: ', x1)
        self.print('Мантисса первого в мoк: ', x2[0] + x2)
        self.print('Мантисса второго в мoк: ', y2[0] + y2)
        self.print(' ', x2[0] + x2)
        self.print('+')
        self.print(' ', y2[0] + y2)
        s = self.plus(x2, y2)
        self.print('-------------')
        self.print(' ', s)

        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)
        s = s[:-1]
        return [s, x1]

    def normal(self, x1, s):
        self.print('Необходима нормализация мантиссы сдвигом влево')
        s = s[:2] + s[3:] + '0'
        if x1 != ('1.' + '1' * (len(x1) - 2)):
            ed = '1.' + '0' * (len(x1) - 3) + '1'
            x1 = self.PinD(x1)
            ed = self.PinD(ed)
            x1 = self.plus(x1, ed)[2:]
            x1 = self.DinP(x1)
        else:
            x1 = '1.1' + '0' * (len(x1) - 2)
        self.print('Смещенная мантисса: ', s)
        self.print('Уменьшенный порядок: ', x1)
        return [x1, s]

    def t_121(self, y1, y2, x2, s, zero, op):
        self.print('[mx]мдк + [-my]мдк = ', s[1:], end='\n')
        self.print('выполним суммирование с 1 пока разность не станет 0')
        while s != zero:
            s = s[2:]
            self.print(' ', s[0] + s)
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s) - 3) + '1')

            s = self.plus(s, '0.' + '0' * (len(s) - 3) + '1')
            x2 = x2[:2] + '0' + x2[2:-1]

            self.print('-------------')
            self.print(' ', s)

        self.print('Смещенное первое [Mx\']пк = ', x2)
        if op == '-':
            y2 = str(1 ^ int(y2[0])) + y2[1:]
            self.print('[-My]пк = ', y2)

        x2, y2 = self.PinO(x2), self.PinO(y2)
        self.print('[Mx\']мок = ', x2[0] + x2)
        self.print('[My]мок = ', y2[0] + y2)
        self.print(' ', x2[0] + x2)
        self.print('+')
        self.print(' ', y2[0] + y2)
        s = self.plus(x2, y2)
        self.print('-------------')
        self.print(' ', s)

        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)

        if s[1:3] == '01':
            s, y1 = self.denormmin(y1, x2, y2)
        elif s[1:3] == '10':
            s, y1 = self.denormplu(y1, x2, y2)

        s = s[2:]
        self.print('сумма в обратном коде: ', s)
        self.print('сумма в прямом коде: ', self.PinO(s))
        s = self.PinO(s)
        if s[2] == '0':
            y1, s = self.normal(y1, s)

        self.print('Искомая сумма: ', y1 + '.' + s)

    def t_122(self, x1, x2, y2, s, zero, op):
        self.print('[mx]мдк + [-my]мдк = ', s[0] + s, end='\n')
        self.print('выполним вычитание с 1 пока разность не станет 0')
        while s != zero:
            self.print(' ', s[0] + s)
            self.print('-')
            self.print(' ', '00.' + '0' * (len(s) - 3) + '1')
            c = 0
            for i in range(len(s) - 1, 1, -1):
                if s[i] == '1':
                    c = i
                    break
            s = s[:c] + '0' + '1' * (len(s) - c - 1)
            self.print('-------------')
            self.print(' ', s)

            y2 = y2[:2] + '0' + y2[2:-1]
        self.print('Смещенное второе [My\']пк = ', y2)

        if op == '-':
            y2 = str(1 ^ int(y2[0])) + y2[1:]
            self.print('[-My\'пк = ', y2)

        x2, y2 = self.PinO(x2), self.PinO(y2)
        self.print('[Mx]мок = ', x2[0] + x2)
        self.print('[-My\']мок = ', y2[0] + y2)
        self.print(' ', x2[0] + x2)
        self.print('+')
        self.print(' ', y2[0] + y2)
        s = self.plus(x2, y2)
        self.print('-------------')
        self.print(' ', s)

        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)

        if (s[1:3] == '01'):
            s, x1 = self.denormmin(x1, x2, y2)
        elif s[1:3] == '10':
            s, x1 = self.denormplu(x1, x2, y2)

        s = s[2:]
        self.print('сумма в обратном коде: ', s)
        self.print('сумма в прямом коде: ', self.PinO(s))
        s = self.PinO(s)

        if s[2] == '0': x1, s = self.normal(x1, s)

        self.print('Искомая сумма: ', x1 + '.' + s)

    def process(self, operation: str, x: str, y: str) -> list:
        """
        ONLY FOR PK
        :param operation: char - (+/-)
        :param x: string operand 1
        :param y: string operand 2
        :return: logs
        """
        assert len(x) == len(y)
        self.reset_logs()
        t_x = x.split('.')
        t_y = y.split('.')
        x1, x2 = t_x[0] + "." + t_x[1], t_x[2] + "." + t_x[3]
        y1, y2 = t_y[0] + "." + t_y[1], t_y[2] + "." + t_y[3]
        self.print('\n\n')

        y3 = str(1 ^ int(y1[0])) + y1[1:]
        self.print('[-my]пк = ', y3)
        x3, y3 = self.PinD(x1), self.PinD(y3)
        self.print('[mx]мдк = ', x3[0] + x3)
        self.print('[-my]мдк = ', y3[0] + y3)
        self.print(' ', x3[0] + x3)
        self.print('+')
        self.print(' ', y3[0] + y3)
        s = self.plus(x3, y3)
        self.print('-------------')
        self.print(' ', s)

        if s[1:3] == '01':
            self.print('Положительное препеолнение -> искомая сумма равна первому числу: ', x1 + '.' + x2)
        elif (s[1:3] == '10') or (s == '111.00'):
            if operation == '+':
                self.print('Отрицательное препеолнение -> искомая сумма равна второму числу: ',
                           y1 + '.' + y2)
            else:
                self.print(
                    'Отрицательное препеолнение -> искомая сумма равна второму числу со знаком минус: ',
                    (y1 + '.' + '0' + y2[1:]) if y2[0] == '1' else (y1 + '.' + '1' + y2[1:]))
        else:
            self.print('\n\n')
            if s[1:3] == '11':
                self.print('mx < my')
                self.t_121(y1, y2, x2, s, '100.' + '0' * (len(y1) - 2), operation)
            else:
                self.print('mx > my')
                self.t_122(x1, x2, y2, s[2:], '0.' + '0' * (len(y1) - 2), operation)

        return self.get_logs()


if __name__ == "__main__":
    t = Task12()
    log = t.process("-", "1.01.0.1101", "0.01.1.1011")
    print("\n".join(log))
