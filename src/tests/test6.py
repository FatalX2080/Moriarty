try:
    from test import AdjacencyTable
    from test5 import Task5v2
except ModuleNotFoundError:
    from .test import AdjacencyTable
    from .test5 import Task5v2


class Task6:  # By @FatalX2080
    def __init__(self):
        self.task5_eng = Task5v2()

    def switch_func(self, fv):
        knf = list(set([str(i) for i in range(16)]) - set(fv))
        knf.sort()
        return knf

    def process(self, x: int, f_values: tuple, x_values: tuple, _: ... = None) -> tuple:
        """
          :param x: count of variables
          :param f_values: tuples of stings 10 base func values (DNF)
          :param x_values: tuples of stings 10 base unknown values
          :param _: plug
          :return: cubes, (adjacency table tata), MdkNF, confirmed state
        """

        sdnf_values = f_values + x_values
        sknf_values = self.switch_func(f_values)

        sdnf_data = self.task5_eng.process(4, tuple(sdnf_values), 1)
        sknf_data = self.task5_eng.process(4, tuple(sknf_values), 0)

        return sdnf_data, sknf_data


if __name__ == "__main__":
    # 4
    # 0 2 8 6
    # 1 3 7
    pass
