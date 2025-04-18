try:
    from test import Supportive
except ModuleNotFoundError:
    from .test import Supportive



class Task8(Supportive):
    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------------------------------------

    def plus(self, a, b):
        prepare = lambda x: '0' + x[0] + x.split('.')[0] + x.split('.')[1]

        a = prepare(a)
        b = prepare(b)
        k = 0
        s = ''
        for i in range(len(a) - 1, -1, -1):
            s = str(int(a[i]) ^ int(b[i]) ^ k) + s
            k = (int(a[i]) & int(b[i])) | (int(a[i]) & k) | (int(b[i]) & k)
        return s[0:3] + '.' + s[3:]

    def __PinO(self, a):
        if a[0] == '0': return a
        return ['1.'] + [str(int(i == '0')) for i in a[2:]]

    def __PinD(self, a):
        if a[0] == '0': return a
        s = self.__PinO(a)
        s = self.plus(s, '0.' + '0' * (len(s) - 3) + '1')
        return 'Overflow' if self.ovf_validate(s) else s[2:]

    def __OinD(self, a):
        if a[0] == '0': return a
        s = self.plus(a, '0.' + '0' * (len(a) - 3) + '1')
        return 'Overflow' if self.ovf_validate(s) else s[2:]

    def __DinP(self, a):
        if a[0] == '0': return a
        c = 0
        for i in range(len(a) - 1, 1, -1):
            if a[i] == '1':
                c = i
                break
        a = a[:c] + '0' + '1' * (len(a) - c - 1)
        return self.__PinO(a)

    def __DinO(self, a):
        if a[0] == '0': return a
        c = 0
        for i in range(len(a) - 1, 1, -1):
            if a[i] == '1':
                c = i
                break
        return a[:c] + '0' + '1' * (len(a) - c - 1)

    def ovf_validate(self, s):
        return s[1:3] not in ['11', '00']

    def pmok_script(self, result_code, operation, a, b):
        if operation == '-':
            b = str(1 ^ int(b[0])) + b[1:]
            self.print('[-Y]пк = ', b)
        a, b = self.__PinO(a), self.__PinO(b)
        text = "число в модифицированном обратном коде: "
        self.print(f'Первое {text}{a[0] + a}')
        self.print(f'Второе {text}{b[0] + b}')
        s = self.plus(a, b)
        self.print(' ', a[0] + a)
        self.print('+')
        self.print(' ', b[0] + b)
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

        if self.ovf_validate(s):
            self.print('Overflow')
        else:
            s = s[2:]
            self.print('сумма в обратном коде: ', s)
            if result_code == 'P':
                self.print('сумма в прямом коде: ', self.__PinO(s))
            elif result_code == 'D':
                self.print('сумма в доп коде: ', self.__OinD(s))

    def pmdk_script(self, result_code, operation, a, b):
        if operation == '-':
            b = str(1 ^ int(b[0])) + b[1:]
            self.print('[-Y]пк = ', b)
        a, b = self.__PinD(a), self.__PinD(b)
        self.print(f'Первое число в модифицированном дополнительном коде: {a[0] + a}')
        self.print(f'Второе число в модифицированном дополнительном коде: {b[0] + b}')
        s = self.plus(a, b)
        self.print(' ', a[0] + a)
        self.print('+')
        self.print(' ', b[0] + b)
        self.print('-------------')
        self.print(' ', s)

        if self.ovf_validate(s):
            self.print('Overflow')
        else:
            s = s[2:]
            self.print('сумма в доп коде: ', s)
            if result_code == 'P':
                self.print('сумма в прямом коде: ', self.__DinP(s))
            elif result_code == 'O':
                self.print('сумма в доп коде: ', self.__DinO(s))

    def dmdk_script(self, result_code, operation, a, b):
        if operation == '-':
            b = self.__DinP(b)
            b = str(1 ^ int(b[0])) + b[1:]
            b = self.__PinD(b)
            self.print('[-Y]дк = ', b)
        s = self.plus(a, b)
        self.print(' ', a[0] + a)
        self.print('+')
        self.print(' ', b[0] + b)
        self.print('-------------')
        self.print(' ', s)

        if self.ovf_validate(s):
            self.print('Overflow')
        else:
            s = s[2:]
            self.print('сумма в доп коде: ', s)
            if result_code == 'P':
                self.print('сумма в прямом коде: ', self.__DinP(s))

    def omok_script(self, result_code, operation, a, b):
        if operation == '-':
            b = self.__PinO(b)
            b = str(1 ^ int(b[0])) + b[1:]
            b = self.__PinO(b)
            self.print('[-Y]oк = ', b)
        s = self.plus(a, b)
        self.print(' ', a[0] + a)
        self.print('+')
        self.print(' ', b[0] + b)
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

        if self.ovf_validate(s):
            self.print('Overflow')
        else:
            s = s[2:]
            self.print('сумма в обратном коде: ', s)
            if result_code == 'P':
                self.print('сумма в прямом коде: ', self.__PinO(s))

    # ------------------------------------------------------------------------------------------------------------------

    def process(self, input_code: str, operation_code: str, result_code: str, operation: str, a: str,
                b: str) -> list:
        """
        :param input_code: char - (p/d/o)
        :param operation_code: string - (mok/mdk)
        :param result_code: char - (p/d/o)
        :param operation: char - (-/+)
        :param a: operand
        :param b: operand
        :return: result of operation
        """
        # TODO НЕ ЗАБУДЬТЕ ЧТО ЕСЛИ В ДК ПОЛУЧИЛОСЬ 111.00..0 ЭТО ТОЖЕ ПЕРЕПОЛНЕНИЕ
        self.reset_logs()
        assert len(a) == len(b)
        script = (input_code + operation_code).lower()
        result_code = result_code.upper()

        match script:
            case "pmok":
                self.pmok_script(result_code, operation, a, b)
            case "pmdk":
                self.pmdk_script(result_code, operation, a, b)
            case "dmdk":
                self.dmdk_script(result_code, operation, a, b)
            case "omok":
                self.omok_script(result_code, operation, a, b)
        return self.get_logs()


if __name__ == "__main__":
    task = Task8()
    logs = task.process("d", "mdk", "p", "+", "1.010100", "1.110000")
    print("\n".join(logs))
