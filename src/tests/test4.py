# BETTA
# TODO пока только для СДНФ
try:
    from test import AdjacencyTable, SdknfGenerator
except ModuleNotFoundError:
    from .test import AdjacencyTable, SdknfGenerator


class Task4:
    def __init__(self, system_call: bool = False):
        self.gluing_flag = True
        self.elements = 0
        self.gen = []
        self.new_gen = []
        self.columns = []

        self.system_call = system_call

        self.dkgen = SdknfGenerator()

    # ------------------------------------------------------------------------------------------------------

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

    def __gen_empty_list(self, l):
        return [[] for _ in range(l)]

    def __gen_mask_list(self, l):
        return [[0] * len(self.gen[_]) for _ in range(l + 1)]

    # ------------------------------------------------------------------------------------------------------
    def _stage0(self, x, f_values) -> list:
        columns = [bin(int(i))[2:].zfill(x) for i in f_values]
        self.elements = x
        self.gen = [[] for _ in range(x + 1)]
        for el in columns:
            self.gen[el.count("1")].append(el)
        return columns

    def _stage1(self, x):
        final_gen = []

        while self.gluing_flag:
            self.gluing_flag = False
            self.new_gen = self.__gen_empty_list(x)
            gen_mask = self.__gen_mask_list(x)
            for iex in range(x):
                for b1_iex, b1 in enumerate(self.gen[iex]):
                    for b2_iex, b2 in enumerate(self.gen[iex + 1]):
                        if self.__merge(b1, b2):
                            gen_mask[iex][b1_iex] = 1
                            gen_mask[iex + 1][b2_iex] = 1

            if any(self.new_gen):
                for i in range(x + 1):
                    for j in range(len(gen_mask[i])):
                        if not gen_mask[i][j]: final_gen.append(self.gen[i][j])
                self.gen = [list(set(r)) for r in self.new_gen]
                x -= 1

        for i in range(x + 1):
            for j in range(len(self.gen[i])):
                final_gen.append(self.gen[i][j])

        return final_gen

    def reset(self):
        self.gluing_flag = True
        self.elements = 0
        self.gen.clear()
        self.columns.clear()
        self.new_gen.clear()

    def process(self, x: int, f_values: tuple) -> str:
        """
        :param x: count of variables
        :param f_values: tuples of stings 10 base func values
        :return: MDNF
        """
        self.reset()
        # --------------------------------------------------------------------------------------------------
        columns = self._stage0(x, f_values)
        rows = self._stage1(x)
        # --------------------------------------------------------------------------------------------------
        tp = AdjacencyTable(columns, rows)
        res_rows = tp.process()
        # --------------------------------------------------------------------------------------------------
        ans = self.dkgen.sdnf(res_rows)
        return ans

    def test5_supportive(self, x: int, f_values: tuple) -> tuple:
        self.reset()
        columns = self._stage0(x, f_values)
        rows = self._stage1(x)
        tp = AdjacencyTable(columns, rows)
        table = tp.get_table()
        res_rows = tp.process()
        return self.dkgen.sdnf(res_rows), (columns, rows), res_rows, table


if __name__ == "__main__":
    t = Task4()

    req1 = t.process(3, ("1", "7"))
    req2 = t.process(3, ("1", "0"))
    req3 = t.process(4, ('9', '11', '12', '14', '15'))

    print(req1)  # (!a*!b*c)+(a*b*c)
    print(req2)  # (!a*!b)
    print(req3)  # (a*!b*d)+(a*b*!d)+(a*c*d)
    print(t.process(4, ("1", "3", "5", "7", "11", "12", "13", "14", "15")))

    assert req1 == "(!a*!b*c)+(a*b*c)"
    assert req2 == "(!a*!b)"
