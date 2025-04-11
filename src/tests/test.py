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

# ----------------------------------------------------------------------------------------------------------
import string


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


# ----------------------------------------------------------------------------------------------------------
def gen_SDNF(rows) -> str:
    res = ""
    alph = string.ascii_lowercase
    for block in rows:
        temp = "("
        i = 0
        for el in block:
            if el != "-":  temp += "!" * (el == "0") + alph[i] + "*"
            i += 1
        res += temp[:-1] + ")+"
    return res[:-1] if res[:-1] != ')' else "VOID"
