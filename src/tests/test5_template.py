import numpy as np


class Task5:
    addressing_N2 = {
        "0": (0, 1),
        "1": (0, 0),
        "2": (1, 1),
        "3": (1, 0),
    }
    addressing_N3 = {
        "0": (1, 3),
        "1": (1, 2),
        "2": (1, 0),
        "3": (1, 1),
        "4": (0, 3),
        "5": (0, 2),
        "6": (0, 0),
        "7": (0, 1)
    }
    addressing_N4 = {
        "0": (3, 3),
        "1": (3, 2),
        "2": (2, 3),
        "3": (2, 2),
        "4": (3, 0),
        "5": (3, 1),
        "6": (2, 0),
        "7": (2, 1),
        "8": (0, 3),
        "9": (0, 2),
        "10": (1, 3),
        "11": (1, 2),
        "12": (0, 0),
        "13": (0, 1),
        "14": (1, 0),
        "15": (1, 1),
    }

    cubes = (
        (4, 4),
        (3, 3),
        (2, 2),

        (1, 4),
        (4, 1),
        (2, 1),
        (1, 2),

        (1, 1),
    )

    def __init__(self):
        self.N = 0
        self.addressing = [Task5.addressing_N2, Task5.addressing_N3, Task5.addressing_N4]

        self.table = None
        self.t_size = ()

    def _create_table(self, values):
        n = self.N - 2
        sizes = [(2, 2), (2, 5), (6, 6)]
        self.t_size = sizes[n]
        self.table = np.zeros(sizes[n], dtype=np.int8)

        address_dict = self.addressing[n]
        for v in values:
            self.table[address_dict[v][0], address_dict[v][1]] = 1

        if n == 1:
            self.table[0:2, 4] = self.table[0:2, 0]
        if n == 2:
            self.__push()

    def __check_cube_fill(self, r, c, mcube):
        return np.sum(self.table[r:r + mcube[0], c:c + mcube[1]]) == mcube[0] * mcube[1]

    def __get_hash(self):
        """
        :return: cols rows
        """
        return np.sum(self.table[:, 4:]), np.sum(self.table[4:, :])

    def __pull(self, old_hash, new_hash):

        if old_hash[0] != new_hash[0] and old_hash[1] != new_hash[1]:
            temp = self.table[4:, 4:]
            self.table[4:, :2] = temp
            self.table[:2, 4:] = temp
            self.table[:2, :2] = temp
        if old_hash[0] != new_hash[0]:
            self.table[:, :2] = self.table[:, 4:]
        elif old_hash[1] != new_hash[1]:
            self.table[:2] = self.table[4:]

    def __push(self):
        temp = self.table[:2, :2]

        self.table[4:] = self.table[:2]
        self.table[:, 4:] = self.table[:, :2]
        self.table[4:, :2] = temp

    def process(self, n: int, func_values: tuple):
        self.N = n
        self._create_table(func_values)

        if np.sum(self.table[:4, :4]) == 16:
            self.table[:4, :4] = -1  # 4x4 m cube

        for r in range(4):
            for c in range(4):
                self.table = np.ones(self.t_size, dtype=np.int8)
                if np.sum(self.table[r:r + 3, c:c + 3]) == 9:
                    self.table[r:r + 3, c:c + 3] = -2  # 3x3 m cube
                    if r == 2: self.table[0, c:c + 3] = -2
                    if c == 2: self.table[r:r + 3, 0] = -2
                    if c == 2 and r == 2: self.table[0, 0] = -2

                    if r == 3:
                        self.table[0:2, c:c + 3] = -2
                        if c == 2:
                            self.table[0, 0] = -2
                    if c == 3:
                        self.table[r:r + 3, 0:2] = -2
                        if r == 2:
                            self.table[0, 0] = -2
                    if c == 3 and r == 3:
                        self.table[0:2, 0:2] = -2


        for r in range(4):
            for c in range(4):
                self.table = np.ones(self.t_size, dtype=np.int8)
                if np.sum(self.table[r:r + 2, c:c + 2]) == 4:
                    self.table[r:r + 2, c:c + 2] = -3  # 2x2 m cube
                    if r == 3: self.table[0, c:c + 2] = -3
                    if c == 3: self.table[r:r + 2, 0] = -3
                    if c == 3 and r == 3: self.table[0, 0] = -3

        for r in range(4):
            if np.sum(self.table[r, :4]) == 4:
                self.table[r, :4] = -4  # 1x4 m cube

        for c in range(4):
            if np.sum(self.table[:4, c]) == 4:
                self.table[:4, c] = -5  # 4x1 m cube

        for r in range(4):
            for c in range(4):
                if np.sum(self.table[r, c:c + 2]) == 2:
                    self.table[r, c:c + 2] = -6  # 1x2 m cube
                    if c == 3:
                        self.table[r, 0] = -6

        for r in range(4):
            for c in range(4):
                if np.sum(self.table[r:r + 4, c]) == 2:
                    self.table[r:r + 4, c] = -7  # 2x1 m cube
                    if r == 3:
                        self.table[0, c] = -7

        a = 0


if __name__ == "__main__":
    t = Task5()
    print(t.process(4, ("1", "3", "5", "7", "11", "12", "13", "14", "15")))
