try:
    from test import Supportive
except ModuleNotFoundError:
    from .test import Supportive


class Task9(Supportive):  # By @XukuM
    def __init__(self):
        super().__init__()

    def get_sign(self, x, y):
        return str(int(x[0]) ^ int(y[0]))

    def minus(self, x):
        return bin(int(''.join([str(int(not int(a))) for a in x]), 2) + 1)[2:].zfill(len(x))

    def sum_prod(self, x, y):
        if len(y) < len(x):
            y += '0' * (len(x) - len(y))
        z = bin(int(x, 2) + int(y, 2))[2:]
        if len(z) < len(x):
            z = '0' * (len(x) - len(z)) + z
        return z[-len(x):]

    def shift_right(self, x, sign, times):
        return sign * times + x

    def print_num(self, x):
        return x[0] + '.' + x[1:]

    # ------------------------------------------------------------------------------------------------------------------
    def __prod_pk_min(self, x, y):
        sign = self.get_sign(x, y)
        self.print(f'Знак = {x[0]} xor {y[0]} = ', sign)
        z = '0' * (len(x))
        x = '0' + x[1:]
        y = '0' + y[1:]
        self.print(' x =', self.print_num(x))
        self.print(' y =', self.print_num(y) + '\n')
        zero = '0' * len(x)

        for i in range(len(y) - 1, 0, -1):
            self.print(f'y{i} = {y[i]}')
            if y[i] == '0':
                self.print(
                    f'   {self.print_num(z)}    S{len(y) - i - 1}\n+  {self.print_num(zero)}    x * y{i}\n   -----')
                z = self.sum_prod(z, zero)
                self.print(f'S{len(y) - i}={self.print_num(z)} -> 0.{z}\n')
                z = self.shift_right(z, '0', 1)
            else:
                self.print(
                    f'   {self.print_num(z)}    S{len(y) - i - 1}\n+  {self.print_num(x)}    x * y{i}\n   -----')
                z = self.sum_prod(z, x)
                self.print(f'S{len(y) - i}={self.print_num(z)} -> 0.{z}\n')
                z = self.shift_right(z, '0', 1)

        return sign + '.' + z[1:]

    def __prod_dk_min(self, x, y):
        z = '0' * (len(x))
        y += '0'
        self.print(' x =', self.print_num(x))
        self.print(' y =', self.print_num(y))
        zero = '0' * len(x)
        mx = self.minus(x)
        self.print('-x =', self.print_num(mx) + '\n')

        ymas = []
        self.print('  y_(n+2-i) - y_(n+1-i)')
        for i in range(len(y) - 1, 0, -1):
            ymas.append(int(y[i]) - int(y[i - 1]))
            self.print(f'i{len(y) - i}  =  ', y[i], '  -  ', y[i - 1], '  =  ', ymas[len(ymas) - 1])
        self.print('\n')

        for i in range(len(ymas)):
            self.print(f'i{i + 1} = {ymas[i]}')
            if ymas[i] == 0:
                self.print(f'   {self.print_num(z)}    S{i}\n+  {self.print_num(zero)}   '
                           f' x * i{i + 1}\n   -----')
                z = self.sum_prod(z, zero)
                self.print(f'S{i}={self.print_num(z)} -> ', z[0] + '.' + z, '\n')
                z = self.shift_right(z, z[0], 1)
            elif ymas[i] == 1:
                self.print(f'   {self.print_num(z)}    S{i}\n+  {self.print_num(x)}   '
                           f' x * i{i + 1}\n   -----')
                z = self.sum_prod(z, x)
                self.print(f'S{i}={self.print_num(z)} -> ', z[0] + '.' + z, '\n')
                z = self.shift_right(z, z[0], 1)

            else:
                self.print(f'   {self.print_num(z)}    S{i}\n+  {self.print_num(mx)}   '
                           f' x * i{i + 1}\n   -----')
                z = self.sum_prod(z, mx)
                self.print(f'S{i}={self.print_num(z)} -> ', z[0] + '.' + z, '\n')
                z = self.shift_right(z, z[0], 1)

        return z[0] + '.' + z[2:]

    # ------------------------------------------------------------------------------------------------------------------

    def __prod_pk_max(self, x, y):
        sign = self.get_sign(x, y)
        self.print(f'Знак = {x[0]} xor {y[0]} = ', sign)
        z = '0' * (len(x))
        x = '0' + x[1:]
        y = '0' + y[1:]
        self.print(' x =', self.print_num(x))
        self.print(' y =', self.print_num(y) + '\n')
        zero = '0' * len(x)
        self.print(f'   {self.print_num(x)}\n*  {self.print_num(y)}\n   ------')
        hist = []
        for i in range(1, len(y)):
            if (y[i] == '0'):
                z = self.sum_prod(self.shift_right(zero, '0', i), z)
                hist.append(z)
                self.print(f'  ', self.print_num(self.shift_right(zero, '0', i)),
                           f'    x * 2^-{i} * y{i}')
            else:
                z = self.sum_prod(self.shift_right(x, '0', i), z)
                hist.append(z)
                self.print(f'  ', self.print_num(self.shift_right(x, '0', i)), f'    x * 2^-{i} * y{i}')
        self.print('  ', '-' * (len(z) + 1))
        self.print('  ', self.print_num(z))
        self.print("История вычисления промежуточных сумм: ")
        for i in range(len(hist)):
            self.print(f'S{i} = {self.print_num(hist[i])}', end='\n')

        return sign + '.' + z[1:]

    def __prod_dk_max(self, x, y):
        z = '0' * (len(x))
        y += '0'
        self.print(' x =', self.print_num(x))
        self.print(' y =', self.print_num(y))
        zero = '0' * len(x)
        mx = self.minus(x)
        self.print('-x =', self.print_num(mx) + '\n')

        hist = []
        ymas = []
        self.print('      y_(i) - y_(i-1)')
        for i in range(1, len(y)):
            ymas.append(int(y[i]) - int(y[i - 1]))
            self.print(f'i{i}  =  ', y[i], '  -  ', y[i - 1], '  =  ', ymas[len(ymas) - 1])
        self.print('\n')

        self.print(f'   {self.print_num(x)}\n*  {self.print_num(y)}\n   ------')
        for i in range(len(ymas)):
            if ymas[i] == 0:
                z = self.sum_prod(self.shift_right(zero, '0', i), z)
                hist.append(z)
                self.print(f'  ', self.print_num(self.shift_right(zero, '0', i)),
                           f'    x * i{i + 1} * 2^-{i}')
            elif ymas[i] == 1:
                z = self.sum_prod(self.shift_right(x, x[0], i), z)
                hist.append(z)
                self.print(f'  ', self.print_num(self.shift_right(x, x[0], i)),
                           f'    x * i{i + 1} * 2^-{i}')
            else:
                z = self.sum_prod(self.shift_right(mx, mx[0], i), z)
                hist.append(z)
                self.print(f'  ', self.print_num(self.shift_right(mx, mx[0], i)),
                           f'    x * i{i + 1} * 2^-{i}')

        self.print('  ', '-' * (len(z) + 1))
        self.print('  ', self.print_num(z))
        self.print("История вычисления промежуточных сумм: ")
        for i in range(len(hist)):
            self.print(f'S{i} = {self.print_num(hist[i])}', end='\n')

        return z[0] + '.' + z[1:]

    def process(self, a, b, values_pass: str, operation_code: str):
        """
        :param a: Operand 1
        :param b: Operand 2
        :param values_pass: char - (y/o)
        :param operation_code: char - (p/d)
        :return: logs
        """
        self.reset_logs()
        a = a.replace('.', '')
        b = b.replace('.', '')
        mode = values_pass + operation_code
        match mode:
            case "yp":
                self.print('Умножение в пк с младших разрядов: ')
                self.print('\nz = ', self.__prod_pk_min(a, b))
            case "op":
                self.print('Умножение в пк со старших разрядов: ')
                self.print('\nz = ', self.__prod_pk_max(a, b))
            case "yd":
                self.print('Умножение в дк с младших разрядов: ')
                self.print('\nВНИМАНИЕ: последний сдвиг лишний')
                self.print('\nz = ', self.__prod_dk_min(a, b))
                self.print('\nВНИМАНИЕ: последний сдвиг лишний')
            case "od":
                self.print('Умножение в дк со старших разрядов: ')
                self.print('\nz = ', self.__prod_dk_max(a, b))

        return self.get_logs()


if __name__ == '__main__':
    test = Task9()
    print(test.process("0.1011", "0.1011", "o", "d")[-1])
    print(test.process("0.1011", "0.1011", "y", "d")[-2])
    print(test.process("0.1011", "0.1011", "o", "p")[-1])
    print(test.process("0.1011", "0.1011", "y", "p")[-1])
