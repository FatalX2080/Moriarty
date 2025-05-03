import string


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
        logs = self.__logs.copy()
        self.__logs.clear()
        return logs

    def reset_logs(self):
        self.__logs = []


class AuxiliaryFunctions:
    def prepare(self, x):
        return '0' + x[0] + x.split('.')[0] + x.split('.')[1]

    def plus(self, a: str, b: str) -> str:
        a = self.prepare(a)
        b = self.prepare(b)
        k = 0
        s = ''
        for i in range(len(a) - 1, -1, -1):
            s = str(int(a[i]) ^ int(b[i]) ^ k) + s
            k = (int(a[i]) & int(b[i])) | (int(a[i]) & k) | (int(b[i]) & k)
        return s[0:3] + '.' + s[3:]

    def PinO(self, a):
        return a if a[0] == '0' else "".join(['1.'] + [str(int(i == '0')) for i in a[2:]])

    def PinD(self, a):
        if a[0] == '0': return a
        s = self.PinO(a)
        s = self.plus(s, '0.' + '0' * (len(s) - 3) + '1')
        return 'Overflow' if self.ovf_validate(s) else s[2:]

    def OinD(self, a):
        if a[0] == '0': return a
        s = self.plus(a, '0.' + '0' * (len(a) - 3) + '1')
        return 'Overflow' if self.ovf_validate(s) else s[2:]

    def DinP(self, a):
        # TODO скорее всего неправильный
        if a[0] == '0': return a
        c = 0
        for i in range(len(a) - 1, 1, -1):
            if a[i] == '1':
                c = i
                break
        a = a[:c] + '0' + '1' * (len(a) - c - 1)
        return self.PinO(a)

    def DinO(self, a):
        if a[0] == '0': return a
        c = 0
        for i in range(len(a) - 1, 1, -1):
            if a[i] == '1':
                c = i
                break
        return a[:c] + '0' + '1' * (len(a) - c - 1)

    def ovf_validate(self, s):
        return s[1:3] not in ['11', '00']


# ----------------------------------------------------------------------------------------------------------


class AdjacencyTable:
    def __init__(self, column, row):
        self.t = None
        self.t_size = ()
        self.rows = row
        self.columns = column

        self.gen_table()

        self.c_col = [0] * self.t_size[1]
        self.c_row = [0] * self.t_size[0]

    def gen_table(self):
        n = len(self.columns)
        m = len(self.rows)
        adjacency_table = [
            [self.__compare(self.columns[j], self.rows[i]) for j in range(n)]
            for i in range(m)
        ]
        self.t = adjacency_table
        self.t_size = (len(self.t), len(self.t[0]))

    # ------------------------------------------------------------------------------------------------------
    def gen_col(self, c_iex) -> list:
        return [self.t[r][c_iex] for r in range(self.t_size[0])]

    def activate_rows(self):
        for r in range(self.t_size[0]):
            if self.c_row[r]:
                for c in range(self.t_size[1]):
                    self.c_col[c] |= self.t[r][c]
                self.t[r] = [0] * self.t_size[1]

    def get_the_used(self) -> list:
        return [self.rows[i] for i in range(self.t_size[0]) if self.c_row[i]]

    def __compare(self, b1, b2) -> int:
        bad_values = [("1", "0"), ("0", "1")]
        res = any([pair in bad_values for pair in zip(b1, b2)])
        return int(not res)

    # ------------------------------------------------------------------------------------------------------
    def recurrent_function(self) -> bool:
        success = False
        for c in range(self.t_size[1]):
            if self.c_col[c]: continue

            col = self.gen_col(c)
            assert sum(col) != 0
            one_cords = [r for r in range(self.t_size[0]) if col[r]]
            one_usages = [sum(self.t[one_cords[r]]) for r in range(len(one_cords))]
            used_row = one_cords[one_usages.index(max(one_usages))]
            self.c_row[used_row] = 1
            self.activate_rows()
            success = True
        return success

    # ------------------------------------------------------------------------------------------------------
    def cyclic_activation(self):
        m = self.t_size[1]
        while (sum(self.c_col) != m) and (self.recurrent_function()): pass

    def linear_activation(self):
        for c in range(self.t_size[1]):
            col = self.gen_col(c)
            if sum(col) == 1:
                iex = col.index(1)
                self.c_row[iex] = 1
                self.c_col[c] = 1
        self.activate_rows()

    def process(self) -> list:
        self.linear_activation()
        self.cyclic_activation()
        return self.get_the_used()

    def get_table(self):
        return self.t.copy()


# ----------------------------------------------------------------------------------------------------------

class DKnfGenerator:
    def __init__(self, mode=1):
        if mode:
            self.alph = string.ascii_lowercase
        else:
            self.alph = [f"x{i}" for i in range(9)]

    def sdnf(self, rows: tuple | list) -> str:
        """
        :param rows: tuple of variables value ([0, 1, 0, 1], [1 0 0 1])
        :return: sdnf function
        """
        res = ""
        for block in rows:
            temp = "("
            for i, el in enumerate(block):
                if el != "-":  temp += "!" * (el == "0") + self.alph[i] + "*"
            res += temp[:-1] + ")+"
        return res[:-1] if res[:-1] != ')' else "VOID"

    def sknf(self, rows: tuple | list) -> str:
        """
        :param rows: tuple of variables value ([0, 1, 0, 1], [1 0 0 1])
        :return: sknf function
        """
        res = ""
        for block in rows:
            temp = "("
            for i, el in enumerate(block):
                if el != "-":  temp += "!" * (el == "1") + self.alph[i] + "+"
            res += temp[:-1] + ")*"
        return res[:-1] if res[:-1] != ')' else "VOID"

    def build_table(self):
        pass

    def __func_decompose(self, f, f_type):
        split_signs = ("+", "*") if f_type else ("*", "+")
        return sorted([sorted(j[1:-1].split(split_signs[0])) for j in f.split(split_signs[1])])

    def compare_functions(self, func1: str, func2: str, f_type: int = 1) -> bool:
        """
        :param func1: comparing function 1
        :param func2: comparing function 2
        :param f_type: 1 - SDNF / 2 - SKNF
        :return: equal functions state
        """
        func_t1 = self.__func_decompose(func1, f_type)
        func_t2 = self.__func_decompose(func2, f_type)
        if len(func_t1) != len(func_t2):
            return False
        return all([j[0] == j[1] for j in zip(func_t1, func_t2)])
