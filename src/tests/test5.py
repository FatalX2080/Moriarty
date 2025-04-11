# ALPHA
# TODO пока только для СДНФ
import numpy as np

try:
    from test import AdjacencyTable, gen_SDNF
except ModuleNotFoundError:
    from .test import AdjacencyTable, gen_SDNF
# ----------------------------------------------------------------------------------------------------------

cubes = (
    (4, 4),
    (3, 3),

    (4, 2),
    (2, 4),
    (2, 4),

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

letter_addresses = {
    (0, 0): np.array([1, 1, 0, 0]),
    (0, 1): np.array([1, 1, 0, 1]),
    (0, 2): np.array([1, 0, 0, 1]),
    (0, 3): np.array([1, 0, 0, 0]),
    (1, 0): np.array([1, 1, 1, 0]),
    (1, 1): np.array([1, 1, 1, 1]),
    (1, 2): np.array([1, 0, 1, 1]),
    (1, 3): np.array([1, 0, 1, 0]),
    (2, 0): np.array([0, 1, 1, 0]),
    (2, 1): np.array([0, 1, 1, 1]),
    (2, 2): np.array([0, 0, 1, 1]),
    (2, 3): np.array([0, 0, 1, 0]),
    (3, 0): np.array([0, 1, 0, 0]),
    (3, 1): np.array([0, 1, 0, 1]),
    (3, 2): np.array([0, 0, 0, 1]),
    (3, 3): np.array([0, 0, 0, 0])
}


# ----------------------------------------------------------------------------------------------------------
class TableProcessor:
    def __init__(self):
        self.table = None
        self.check_table = None

    def set_zone(self, r, c, cube, v=0):
        hashes = self.get_hash()
        self.table[r:r + cube[0], c:c + cube[1]] = v
        new_hash = self.get_hash()

        if hashes[0] != new_hash[0]:
            self.table[:2, 4:] = self.table[:2, :2]
            self.table[4:, :2] = self.table[:2, :2]
            self.table[4:, 4:] = self.table[:2, :2]

        if hashes[1] != new_hash[1]:
            self.table[4:, 2:4] = self.table[:2, 2:4]

        if hashes[2] != new_hash[2]:
            self.table[:2, :2] = self.table[:2, 4:]
            self.table[4:, :2] = self.table[:2, 4:]
            self.table[4:, 4:] = self.table[:2, 4:]

        if hashes[3] != new_hash[3]:
            self.table[2:4, 4:] = self.table[2:4, :2]

        if hashes[4] != new_hash[4]:
            self.table[2:4, :2] = self.table[2:4, 4:]

        if hashes[5] != new_hash[5]:
            self.table[0:2, 4:] = self.table[4:, :2]
            self.table[:2, :2] = self.table[4:, :2]
            self.table[4:, 4:] = self.table[4:, :2]

        if hashes[6] != new_hash[6]:
            self.table[:2, 2:4] = self.table[4:, 2:4]

        if hashes[7] != new_hash[7]:
            self.table[0:2, 4:] = self.table[4:, 4:]
            self.table[4:, 0:2] = self.table[4:, 4:]
            self.table[:2, :2] = self.table[4:, 4:]

    def get_hash(self):
        hashes = []
        for r in [0, 1, 2]:
            for c in [0, 1, 2]:
                if r != 1 or c != 1:
                    hashes.append(np.sum(self.table[r * 2:(r + 1) * 2, c * 2:(c + 1) * 2]))
        return hashes

    def check_cube(self, table, r, c, mcube):
        return np.sum(table[r:r + mcube[0], c:c + mcube[1]]) == mcube[0] * mcube[1]


class Coverage(TableProcessor):
    def __init__(self, table: np.array):
        super().__init__()
        self.table = table
        self.check_table = table.copy()

        self.used = []

    def fill_cell(self, r, c):

        border_size = -1
        for cube in cubes:
            if cube[0] * cube[1] < border_size:
                return

            for x in range(cube[0] - 1, -1, -1):
                for y in range(cube[1] - 1, -1, -1):
                    r_cord = max(0, r - x)
                    c_cord = max(0, c - y)
                    if (cube[0] == 4 and r_cord > 0) or (cube[1] == 4 and c_cord > 0):
                        continue
                    if self.check_cube(self.check_table, r_cord, c_cord, cube):
                        self.set_zone(r_cord, c_cord, cube)
                        self.used.append((r_cord, c_cord, cube))

    def process(self) -> list:
        for row in range(3, -1, -1):
            for col in range(3, -1, -1):
                if self.table[row, col] == 1:
                    self.fill_cell(row, col)

        del_indexes = set()
        used_len = len(self.used)
        for i in range(used_len):
            cube0 = self.used[i]
            x0, y0, xs0, ys0 = cube0[0], cube0[1], cube0[2][0], cube0[2][1]
            for j in range(i, used_len):
                if i != j:
                    cube1 = self.used[j]
                    x1, y1, xs1, ys1 = cube1[0], cube1[1], cube1[2][0], cube1[2][1]
                    if (x1 == x0 and y1 == y0) and (
                            xs0 * ys0 > xs1 * ys1 or (xs0 == xs1 and ys0 == ys1)):
                        del_indexes.add(j)

        for iex in list(sorted(list(del_indexes), reverse=True)):
            del self.used[iex]

        return self.used


class Overlap(TableProcessor):
    def __init__(self, usages: list):
        super().__init__()
        self.usages = usages
        self.table = np.zeros((6, 6), dtype=np.int8)

    def nesting_checking(self):
        pr_len = len(self.usages)
        del_indexes = set()
        for i in range(pr_len):

            freeze = self.usages[i]
            x0, y0, cube = freeze
            t1 = np.zeros((6, 6), dtype=np.int8)
            t1[x0:x0 + cube[0], y0:y0 + cube[1]] = 1

            for j in range(pr_len):
                if i != j:
                    self.table[:, :] = 0
                    self.set_zone(*self.usages[j], 1)

                    if np.all((t1 == 1) <= (self.table == 1)):
                        del_indexes.add(i)

        for iex in list(sorted(list(del_indexes), reverse=True)):
            del self.usages[iex]

    def checking_the_overlap(self):
        res = []

        pr_len = len(self.usages)
        for i in range(pr_len):
            self.table[:, :] = 0
            freeze = self.usages[i]
            for j in range(pr_len):
                if i != j:
                    self.set_zone(*self.usages[j], 1)

            fr, fc, fcb = freeze
            if not self.check_cube(self.table, fr, fc, fcb):
                res.append(freeze)

        if not res: res = self.usages

        self.usages = res

    def process(self):
        self.nesting_checking()
        self.checking_the_overlap()
        return self.usages


class SequenceGeneration:

    def __init__(self, mcubes, fval):
        self.mcubes = mcubes
        self.fval = fval

    def gen_bunch(self, mc) -> str:
        cube_letters = []
        x0, y0, mcube = mc
        for r in range(mcube[0]):
            for c in range(mcube[1]):
                cube_letters.append(letter_addresses[((x0 + r) % 4, (y0 + c) % 4)])

        columns = np.array(cube_letters).T
        flags = (np.any(columns, axis=1) == 0) + (np.all(columns, axis=1))
        # a b c d
        bunch = [str(cube_letters[0][f]) if flags[f] else "-" for f in range(4)]
        return "".join(bunch)

    def process(self) -> tuple:
        res = []

        for mc in self.mcubes:
            bunch = self.gen_bunch(mc)
            res.append(bunch)

        columns = [bin(int(fv))[2:].zfill(4) for fv in self.fval]
        t_processor = AdjacencyTable(columns, res)
        ls = t_processor.process()
        return columns, res, ls


class Task5:
    def __init__(self):
        self.table = None

    def create_table(self, values):
        self.table = np.zeros((6, 6), dtype=np.int8)

        for v in values: self.table[*addressing[v]] = 1

        self.table[4:] = self.table[:2]
        self.table[:, 4:] = self.table[:, :2]
        self.table[4:, :2] = self.table[:2, :2]

    def reset(self):
        self.table = None

    # ------------------------------------------------------------------------------------------------------
    def process(self, n: int, func_values: tuple):
        self.reset()

        self.create_table(func_values)

        cov_engine = Coverage(self.table)
        preliminary_list = cov_engine.process()

        over_engine = Overlap(preliminary_list)
        usages = over_engine.process()

        seq_engine = SequenceGeneration(usages, func_values)
        column, res, used_list = seq_engine.process()

        ans = gen_SDNF(used_list)

        return usages, ans


# ----------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    t = Task5()
    print(t.process(4, ("0", "4", "8")))
    print(t.process(4, ("0", "2", "4", "6", "8", "10")))
    print(t.process(4, ("1", "3", "5", "7", "11", "12", "13", "14", "15")))
    print(t.process(4, ("1", "3", "5", "9", "10", "11", "13", "14", "15")))
    #print(t.process(4, tuple("0 1 2 3 9 11 6 7 14 15 10".split())))
    """"1 3 5 7 11 12 13 14 15"""
    """"1 3 5 9 10 11 13 14 15"""
    """0 2 4 6 8 10 """
    """0 1 2 3 9 11 6 7 14 15 10"""
    """
    1 1 . .
    1 1 1 . 
    . 1 1 .
    . 1 1 .
    """
