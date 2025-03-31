# BETTA

import string


class TableProcessor:
    def __init__(self, t, c, r):
        self.t = t
        self.t_size = (len(self.t), len(self.t[0]))
        self.rows = r
        self.columns = c

        self.c_col = [0] * self.t_size[1]
        self.c_row = [0] * self.t_size[0]

    def gen_col(self, c_iex) -> list:
        return [self.t[r][c_iex] for r in range(self.t_size[0])]

    def recurrent_activation(self):
        success = False
        while success:
            success = False
            for c in range(self.t_size[1]):
                if self.c_col[c] == 0:
                    col = self.gen_col(c)
                    assert sum(col) != 0
                    one_cords = [r for r in range(self.t_size[0]) if col[r]]
                    one_usages = [sum(self.t[one_cords[r]]) for r in range(len(one_cords))]
                    used_row = one_cords[one_usages.index(max(one_usages))]
                    self.c_row[used_row] = 1
                    self.activate_rows()
                    success = True

    def activate_rows(self):
        for r in range(self.t_size[0]):
            if self.c_row[r] == 1:
                for c in range(self.t_size[1]):
                    if self.t[r][c] == 1: self.c_col[c] = 1
                self.t[r] = [0] * self.t_size[1]

    def process(self) -> list:
        m = self.t_size[1]

        for c in range(m):
            col = self.gen_col(c)
            if sum(col) == 1:
                iex = col.index(1)
                self.c_row[iex] = 1
                self.c_col[c] = 1

        self.activate_rows()
        if sum(self.c_col) != m: self.recurrent_activation()
        return [self.rows[i] for i in range(self.t_size[0]) if self.c_row[i]]


class Task4:
    def __init__(self):
        self.gluing_flag = True
        self.elements = 0
        self.gen = []
        self.new_gen = []

    def __merge(self, b1, b2) -> bool:
        b3 = ""
        comp = 0
        for el in range(self.elements):
            j = min(b1[el], b2[el]) + max(b1[el], b2[el])
            if j in ["-0", "-1"]:
                return False
            elif j == "01":
                comp += 1
                b3 += "-"
            else:
                b3 += j[0]

        if comp == 1:
            self.new_gen[b3.count("1")].append(b3)
            self.gluing_flag = True
            return True
        return False

    def __compare(self, b1, b2) -> bool:
        for el in range(self.elements):
            if b1[el] + b2[el] in ["10", "01"]: return False
        return True

    def _stage1(self, x):
        final_gen = []

        while self.gluing_flag:
            self.gluing_flag = False
            self.new_gen = [[] for _ in range(x)]
            gen_mask = [[0] * len(self.gen[_]) for _ in range(x + 1)]
            for iex in range(x):
                for b1_iex, b1 in enumerate(self.gen[iex]):
                    for b2_iex, b2 in enumerate(self.gen[iex + 1]):
                        if self.__merge(b1, b2):
                            gen_mask[iex][b1_iex] = 1
                            gen_mask[iex + 1][b2_iex] = 1

            if any([_ for _ in self.new_gen]):
                for i in range(x + 1):
                    for j in range(len(gen_mask[i])):
                        if not gen_mask[i][j]:
                            v = self.gen[i][j]
                            final_gen.append(v)
                self.gen = [list(set(r)) for r in self.new_gen]
                x -= 1

        for i in range(x + 1):
            for j in range(len(self.gen[i])):
                final_gen.append(self.gen[i][j])

        return final_gen

    def _stage2(self, row, cols) -> list:
        n = len(cols)
        m = len(row)

        t = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                t[i][j] = int(self.__compare(cols[j], row[i]))

        return t

    def _stage3(self, r) -> str:
        res = ""
        alph = string.ascii_lowercase
        for block in r:
            temp = "("
            i = 0
            for el in block:
                if el != "-":
                    if el == "0":
                        temp += "!"
                    temp += alph[i] + "*"
                i += 1
            temp = temp[:-1] + ")+"
            res += temp
        if res[:-1] != ')':
            return res[:-1]
        else:
            return "VOID"

    def reset(self):
        self.gluing_flag = True
        self.elements = 0
        self.gen = []
        self.new_gen = []

    def process(self, x: int, f_values: tuple):
        self.reset()
        columns = [bin(int(i))[2:].zfill(x) for i in f_values]
        self.elements = x
        self.gen = [[] for _ in range(x + 1)]
        for el in columns:
            self.gen[el.count("1")].append(el)
        # --------------------------------------------------------------------------------------------------
        rows = self._stage1(x)
        table = self._stage2(rows, columns)
        # --------------------------------------------------------------------------------------------------
        tPr = TableProcessor(table, columns, rows)
        res_rows = tPr.process()
        # --------------------------------------------------------------------------------------------------
        ans = self._stage3(res_rows)

        return ans


if __name__ == "__main__":
    mytest = Task4()
    print(mytest.process(3, ("1", "7")))
    print(mytest.process(3, ("1", "0")))
