from itertools import product
from string import ascii_lowercase

class Task3:
    def __init__(self):
        self.functions = ['', '']  # SKNF / SDNF

    def reset(self):
        self.functions = ['', '']

    def process(self, x: int, f_values: tuple) -> tuple:
        """
        :param x: count of variables
        :param f_values: tuple of function values
        :return: (SDNF, SKNF)
        """
        self.reset()
        a = ascii_lowercase
        variables_set = product((0, 1), repeat=x)
        for i, item in enumerate(variables_set):
            self.functions[f_values[i]] += '('
            for j in range(x):
                self.functions[f_values[i]] += '!' * (item[j] != f_values[i]) + a[j] + '+*'[f_values[i]]
            self.functions[f_values[i]] = self.functions[f_values[i]][:-1] + ')' + "*+"[f_values[i]]

        #SDNF SKNF
        return self.functions[1][:-1], self.functions[0][:-1]


if __name__ == '__main__':
    t = Task3()
    print(t.process(3, (0, 1, 0, 0, 1, 0, 1, 0)))
    print(t.process(3, (0, 1, 0, 0, 1, 0, 1, 0)))