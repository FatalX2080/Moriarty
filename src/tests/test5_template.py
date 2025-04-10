import numpy as np

cubes = (
    (4, 4),
    (3, 3),

    (1, 4),
    (4, 1),
    (2, 2),

    (2, 1),
    (1, 2),

    (1, 1),
)

addressing = {
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


class Coverage:
    def __init__(self, table: np.array):
        self.table = table
        self.check_table = table.copy()
        self.t_size = ()

        self.used = []

    def fill_cell(self, r, c):
        # r, c - координаты проверяемой точки
        for cube in cubes:
            used_cods = set()
            for x in range(cube[0]):
                for y in range(cube[1]):
                    r_cord = max(0, r - x)
                    c_cord = max(0, c - y)

                    if self.__check_cube(r_cord, c_cord, cube):
                        a = 0
                        self.reset_zone(r_cord, c_cord, cube)
                        self.used.append((r_cord, c_cord, cube))
                        return

    def reset_zone(self, r, c, cube):
        hashes = self.get_hash()
        self.table[r:r + cube[0], c:c + cube[1]] = 0
        new_hash = self.get_hash()

        if hashes[0] != new_hash[0]:
            self.table[0:2, 4:] = 0
            self.table[4:, 0:2] = 0
            self.table[4:, 4:] = 0

        if hashes[1] != new_hash[1]:
            self.table[4:, 2:4] = 0

        if hashes[2] != new_hash[2]:
            self.table[:2, :2] = 0
            self.table[4:, 0:2] = 0
            self.table[4:, 4:] = 0

        if hashes[3] != new_hash[3]:
            self.table[2:4, 4:] = 0

        if hashes[4] != new_hash[4]:
            self.table[2:4, :2] = 0

        if hashes[5] != new_hash[5]:
            self.table[0:2, 4:] = 0
            self.table[:2, :2] = 0
            self.table[4:, 4:] = 0

        if hashes[6] != new_hash[6]:
            self.table[:2, 2:4] = 0

        if hashes[7] != new_hash[7]:
            self.table[0:2, 4:] = 0
            self.table[4:, 0:2] = 0
            self.table[:2, :2] = 0

    def get_hash(self):
        hashes = []
        for r in [0, 1, 2]:
            for c in [0, 1, 2]:
                if r != 1 or c != 1:
                    hashes.append(np.sum(self.table[r * 2:(r + 1) * 2, c * 2:(c + 1) * 2]))
        return hashes

    # ------------------------------------------------------------------------------------------------------
    def __check_cube(self, r, c, mcube):
        return np.sum(self.check_table[r:r + mcube[0], c:c + mcube[1]]) == mcube[0] * mcube[1]

    # ------------------------------------------------------------------------------------------------------
    def process(self) -> list:
        for row in range(4):
            for col in range(4):
                if self.table[row, col] == 1:
                    self.fill_cell(row, col)

        return self.used


class Task5:
    def __init__(self):
        self.table = None
        self.check_table = None
        self.t_size = ()

        self.used = []

    def create_table(self, values):
        self.t_size = (6, 6)
        self.table = np.zeros(self.t_size, dtype=np.int8)

        for v in values: self.table[*addressing[v]] = 1

        self.expand()
        self.check_table = self.table.copy()

    def expand(self):
        temp = self.table[:2, :2]

        self.table[4:] = self.table[:2]
        self.table[:, 4:] = self.table[:, :2]
        self.table[4:, :2] = temp

    def fill_cell(self, r, c):
        # r, c - координаты проверяемой точки
        for cube in cubes:
            used_cods = set()
            for x in range(cube[0]):
                for y in range(cube[1]):
                    r_cord = max(0, r - x)
                    c_cord = max(0, c - y)

                    if self.__check_cube(r_cord, c_cord, cube):
                        a = 0
                        self.reset_zone(r_cord, c_cord, cube)
                        self.used.append((r_cord, c_cord, cube))
                        return

    def reset_zone(self, r, c, cube):
        hashes = self.get_hash()
        self.table[r:r + cube[0], c:c + cube[1]] = 0
        new_hash = self.get_hash()

        if hashes[0] != new_hash[0]:
            self.table[0:2, 4:] = 0
            self.table[4:, 0:2] = 0
            self.table[4:, 4:] = 0

        if hashes[1] != new_hash[1]:
            self.table[4:, 2:4] = 0

        if hashes[2] != new_hash[2]:
            self.table[:2, :2] = 0
            self.table[4:, 0:2] = 0
            self.table[4:, 4:] = 0

        if hashes[3] != new_hash[3]:
            self.table[2:4, 4:] = 0

        if hashes[4] != new_hash[4]:
            self.table[2:4, :2] = 0

        if hashes[5] != new_hash[5]:
            self.table[0:2, 4:] = 0
            self.table[:2, :2] = 0
            self.table[4:, 4:] = 0

        if hashes[6] != new_hash[6]:
            self.table[:2, 2:4] = 0

        if hashes[7] != new_hash[7]:
            self.table[0:2, 4:] = 0
            self.table[4:, 0:2] = 0
            self.table[:2, :2] = 0

    def get_hash(self):
        hashes = []
        for r in [0, 1, 2]:
            for c in [0, 1, 2]:
                if r != 1 or c != 1:
                    hashes.append(np.sum(self.table[r * 2:(r + 1) * 2, c * 2:(c + 1) * 2]))
        return hashes

    # ------------------------------------------------------------------------------------------------------
    def __check_cube(self, r, c, mcube):
        return np.sum(self.check_table[r:r + mcube[0], c:c + mcube[1]]) == mcube[0] * mcube[1]

    # ------------------------------------------------------------------------------------------------------
    def process(self, n: int, func_values: tuple):
        self.create_table(func_values)

        for row in range(4):
            for col in range(4):
                if self.table[row, col] == 1:
                    self.fill_cell(row, col)

        print(self.used)


if __name__ == "__main__":
    t = Task5()
    print(t.process(4, ("1", "3", "5", "7", "11", "12", "13", "14", "15")))
