try:
    from test import Supportive, AuxiliaryFunctions
except ModuleNotFoundError:
    from .test import Supportive, AuxiliaryFunctions



class Task8(Supportive, AuxiliaryFunctions):
    def __init__(self):
        super().__init__()

    # ------------------------------------------------------------------------------------------------------
    def pmok_script(self, result_code, operation, a, b):
        if operation == '-':
            b = str(1 ^ int(b[0])) + b[1:]
            self.print('[-Y]пк = ', b)
        a, b = self.PinO(a), self.PinO(b)
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
                self.print('сумма в прямом коде: ', self.PinO(s))
            elif result_code == 'D':
                self.print('сумма в доп коде: ', self.OinD(s))

    def pmdk_script(self, result_code, operation, a, b):
        if operation == '-':
            b = str(1 ^ int(b[0])) + b[1:]
            self.print('[-Y]пк = ', b)
        a, b = self.PinD(a), self.PinD(b)
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
                self.print('сумма в прямом коде: ', self.DinP(s))
            elif result_code == 'O':
                self.print('сумма в доп коде: ', self.DinO(s))

    def dmdk_script(self, result_code, operation, a, b):
        if operation == '-':
            b = self.DinP(b)
            b = str(1 ^ int(b[0])) + b[1:]
            b = self.PinD(b)
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
                self.print('сумма в прямом коде: ', self.DinP(s))

    def omok_script(self, result_code, operation, a, b):
        if operation == '-':
            b = self.PinO(b)
            b = str(1 ^ int(b[0])) + b[1:]
            b = self.PinO(b)
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
                self.print('сумма в прямом коде: ', self.PinO(s))

    # ------------------------------------------------------------------------------------------------------

    def process(self, input_code: str, operation_code: str, result_code: str, operation: str, a: str,
                b: str) -> list:
        """
        :param input_code: char - (p/d/o)
        :param operation_code: string - (mok/mdk)
        :param result_code: char - (p/d/o)
        :param operation: char - (-/+)
        :param a: operand
        :param b: operand
        :return: logs
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
