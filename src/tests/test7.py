try:
    from test import Supportive
except ModuleNotFoundError:
    from .test import Supportive


class Task7(Supportive):
    def __init__(self):
        super().__init__()

    def __to_dop_code(self, x, sign):
        if str(sign) == '0': return x
        inv_v = ''.join([str(int(not int(a))) for a in x])
        bin_v = bin(int(inv_v, 2) + 1)[2:]
        return bin_v.zfill(len(x))

    def process(self, x: str, m: int, digits_count: int) -> list:
        self.reset_logs()
        mant_sign = int(x.startswith('+'))
        x = x.lstrip('-').lstrip('+')

        integer_part, f = x.split('.')
        integer_part = int(integer_part)

        self.print(f'{integer_part}₁₀ = {bin(integer_part)[2:]}₂')
        if integer_part == 0:
            res = ''
            exp = 0
        else:
            res =  bin(integer_part)[2:]
            exp = len(res)

        self.print(f'exp = {exp}\n')

        f_len = len(f)
        f = float('0.' + f)
        self.print(f'    {f:.{f_len}f}')
        while len(res) < digits_count + 1:
            self.print(f'    --{"-" * f_len}')
            f *= 2
            i = int(f)
            if res == '' and i == 0:
                exp -= 1
                self.print(f'    {f:.{f_len}f} -> -')
                f -= i
                self.print(f'    {f:.{f_len}f}    (exp -= 1 : exp = {exp})')
            else:
                res += str(i)
                self.print(f'    {f:.{f_len}f} -> {i}')
                f -= i
                self.print(f'    {f:.{f_len}f}')

        self.print()
        self.print(f'мантисса: {res}')
        round_bit = res[-1]
        res = res[:-1]
        self.print(f'бит округления: {round_bit}')
        z = bin(int(res, 2) + int(round_bit, 2))[2:]
        res, carry = z[-len(x):], z[:-len(x)]
        self.print(f'мантисса + округление: {res}')
        if carry:
            self.print(f'!переполнение при округлении!: {carry}')
            return self.get_logs()

        en = exp + 2 ** (m - 1)
        self.print(f'\nмантисса: {res}')
        self.print(f'экспонента: {exp}')
        self.print(f'm_маш = {en}₁₀ = {bin(en).replace("0b", "")}₂')
        self.print(f'ПК: 0.{bin(en)[2:]}.{mant_sign}.{res}')
        self.print(f'ДК: 0.{bin(en)[2:]}.{mant_sign}.{self.__to_dop_code(res, mant_sign)}')
        return self.get_logs()

if __name__ == '__main__':
    t = Task7()
    print("\n".join(t.process('-38.47', 5, 16)))
