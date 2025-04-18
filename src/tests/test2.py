from math import floor
from .test import Supportive

class Task2(Supportive):
    def __init__(self):
        super().__init__()
        self.s2i = {iex: litter for litter, iex in enumerate("0123456789abcdef")}

    def __convert_float(self, s, base):
        ret = 0
        bef, aft = s, ''
        if "." in s:
            bef, aft = s.split(".")
        for i in enumerate(reversed(bef)):
            integer = self.s2i[i[1]]
            if integer >= base: raise ValueError
            ret += base ** i[0] * integer
        if "." in s:
            for i in enumerate(aft):
                integer = self.s2i[i[1]]
                if integer >= base: raise ValueError
                ret += base ** -(i[0] + 1) * integer
        return ret

    def process(self, x: str, base_x: int, base_ans: int, lg_x: float, lg_ans: float) -> tuple:
        """
        :param x: start value
        :param base_x: base x
        :param base_ans: base answer
        :param lg_x: log x
        :param lg_ans: log ans
        :return: (digits after point, new digits after point, base, answer)
        """
        self.reset_logs()
        n1 = len(x.split('.')[1]) if "." in x else 0
        number_count = floor(n1 * float(lg_x) / float(lg_ans)) + 1
        answer_dec = self.__convert_float(x, base_x)
        answer_dec_bef, answer_dec_aft = str(answer_dec).split(".")
        answer_dec_bef = int(answer_dec_bef)
        answer_dec_aft = float(answer_dec_aft) / 10 ** (len(answer_dec_aft))
        answer_bef, answer_aft = "", ""
        while answer_dec_bef != 0:
            answer_bef = str(answer_dec_bef % base_ans) + answer_bef
            answer_dec_bef //= base_ans

        while len(answer_aft) != number_count + 1:
            answer_dec_aft *= base_ans
            answer_aft += str(int(answer_dec_aft))
            answer_dec_aft -= int(answer_dec_aft)

        # num_after_point_count_old, num_after_point_count_new, base_ans, ans
        self.print('{0}.{1}'.format(answer_bef, answer_aft))
        return n1, number_count, base_ans, self.get_logs()


if __name__ == '__main__':
    t = Task2()
    print(t.process('110101001.0101110010', 2, 5, 0.3010, 0.6990))
    print(t.process('110101001.0101110010', 2, 5, 0.3010, 0.6990))
