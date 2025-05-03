try:
    from test import Supportive, AuxiliaryFunctions
except ModuleNotFoundError:
    from .test import Supportive, AuxiliaryFunctions


class Task11(Supportive, AuxiliaryFunctions):  # By @Sarkoxed
    def script_p(self, x, y):
        y1 = y
        x, y = self.PinO(x), self.PinO(y)
        self.print('[mx]мок = ', x[0] + x)
        self.print('[my]мок = ', y[0] + y)
        s = self.plus(x, y)
        self.print(' ', x[0] + x)
        self.print('+')
        self.print(' ', y[0] + y)
        self.print('---------')
        self.print(s[1:])

        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)

        self.print('\n\n')
        if (s[1:3] != '11') and (s[1:3] != '00'):
            self.print('Overflow при произведении положиельное если 01 и отрицательное наоборот\n')
        else:
            self.print('[mxy]п = ', self.PinO(s[2:]), end='\n')

        self.print('\n')

        y1 = str(1 ^ int(y1[0])) + y1[1:]
        self.print('[-my]п = ', y1)
        y1 = self.PinO(y1)
        self.print('[-my]мок = ', y1[0] + y1)

        s = self.plus(x, y1)
        self.print(' ', x[0] + x)
        self.print('+')
        self.print(' ', y1[0] + y1)
        self.print('---------')
        self.print(s[1:])
        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)

        self.print('\n\n')
        if (s[1:3] != '11') and (s[1:3] != '00'):
            self.print('Overflow при делении положиельное если 01 и отрицательное наоборот\n')
        else:
            s = s[2:]
            self.print('[mx/y]п = ', self.PinO(s), end='\n')

    def script_o(self, x, y):
        self.print('[mx]мок = ', x[0] + x)
        self.print('[my]мок = ', y[0] + y)
        s = self.plus(x, y)
        self.print(' ', x[0] + x)
        self.print('+')
        self.print(' ', y[0] + y)
        self.print('---------')
        self.print(s[1:])

        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)

        self.print('\n')
        if (s[1:3] != '11') and (s[1:3] != '00'):
            self.print('Overflow при произведении положиельное если 01 и отрицательное наоборот\n')
        else:
            self.print('[mxy]o = ', s[2:], end='\n')
        self.print('\n')

        y1 = self.PinO(y)
        y1 = str(1 ^ int(y1[0])) + y1[1:]
        y1 = self.PinO(y1)
        self.print('[-my]o = ', y1)

        self.print('[-my]мок = ', y1[0] + y1)

        s = self.plus(x, y1)
        self.print(' ', x[0] + x)
        self.print('+')
        self.print(' ', y1[0] + y1)
        self.print('---------')
        self.print(s[1:])

        if s[0] == '1':
            self.print('\n')
            self.print(' ', s[1:])
            self.print('+')
            self.print(' ', '00.' + '0' * (len(s[1:]) - 4) + '1')
            s = self.plus(s[2:], '0.' + '0' * (len(s[1:]) - 4) + '1')
            self.print('-------------')
            self.print(' ', s)

        self.print('\n')
        if (s[1:3] != '11') and (s[1:3] != '00'):
            self.print('Overflow при делении положиельное если 01 и отрицательное наоборот\n')
        else:
            self.print('[mx/y]п = ', s[2:], end='\n')

    def script_d(self, x, y):
        self.print('[mx]мдк = ', x[0] + x)
        self.print('[my]мдк = ', y[0] + y)
        s = self.plus(x, y)
        self.print(' ', x[0] + x)
        self.print('+')
        self.print(' ', y[0] + y)
        self.print('---------')
        self.print(s[1:])

        self.print('\n')
        if (s[1:3] != '11') and (s[1:3] != '00'):
            self.print('Overflow при произведении положиельное если 01 и отрицательное наоборот\n')
        else:
            self.print('[mxy]д = ', s[2:], end='\n')
        self.print('\n')

        y1 = self.DinP(y)
        y1 = str(1 ^ int(y1[0])) + y1[1:]
        y1 = self.PinD(y1)
        self.print('[-my]д = ', y1)

        self.print('[-my]мдк = ', y1[0] + y1)

        s = self.plus(x, y1)
        self.print(' ', x[0] + x)
        self.print('+')
        self.print(' ', y1[0] + y1)
        self.print('---------')
        self.print(s[1:])

        self.print('\n')
        if (s[1:3] != '11') and (s[1:3] != '00'):
            self.print('Overflow при делении положительное если 01 и отрицательное наоборот\n')
        else:
            self.print('[mx/y]д = ', s[2:], end='\n')

    def part1(self, code: str, x: str, y: str) -> None:
        """
        :param code: char - (p/d/p)
        :param x: Operand 1
        :param y: Operand 2
        :return:
        """
        code = code.lower()
        match code:
            case 'p':
                self.script_p(x, y)
            case 'o':
                self.script_o(x, y)
            case 'd':
                self.script_d(x, y)

    def part2(self, ma: int, x: str, y: str) -> None:
        """
        :param ma: machine number
        :param x: Operand 1
        :param y: Operand 2
        :return: None
        """
        x1, y1 = int(x, 2), int(y, 2)
        a = x1 + y1 - 2 ** (ma - 1)
        self.print(f'[mxy]M = {x1} + {y1} - 2**({ma}-1) = ', a)
        if a > 2 ** ma:
            self.print('overflow положительное')
        elif a < 0:
            self.print('overflow отрицательное')
            self.print('\n[mxy]M = ', bin(a)[2:][0] + '.' + bin(a)[2:][1:])
        else:
            c = bin(a)[2:]
            self.print('\n[mxy]M = ', '0' * (ma - len(c)) + c)
        b = x1 - y1 + 2 ** (ma - 1)
        self.print(f'\n[mx/y]M = {x1} - {y1} + 2**({ma}-1) = ', b)
        if b > 2 ** ma:
            self.print('overflow положительное')
            self.print('\n[mxy]M = ', bin(b)[2:][0] + '.' + bin(b)[2:][1:])
        elif b < 0:
            self.print('overflow отрицательное')
        else:
            c = bin(b)[2:]
            self.print('\n[mxy]M = ', '0' * (ma - len(c)) + c)

    def process(self, code: str, x1: str, y1: str, x2: str, y2: str) -> list:
        """
        :param code: char - (p/d/o)
        :param x1:  Operand 1 (part 1)
        :param y1:  Operand 1 (part 1)
        :param x2:  Operand 1 (part 2)
        :param y2:  Operand 2 (part 2)
        :return: logs
        """
        self.reset_logs()
        assert len(x2) == len(y2)
        ma = len(x2)
        self.part1(code, x1, y1)
        self.part2(ma, x2, y2)
        return self.get_logs()


if __name__ == '__main__':
    t = Task11()
    logs = t.process("o", "0.110", "1.100", "1111", "0110")
    print("\n".join(logs))
