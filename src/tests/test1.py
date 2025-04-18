from string import ascii_lowercase


class Task1:  # By @FatalX2080
    # If you aren't so lasy as me, you can make it manually (bitwise addition)
    def __init__(self):
        self.values = ()
        self.x = 0
        self.y = 0
        self.res = ""
        self.system = 10
        self.dict = ascii_lowercase

    def __to_decimal(self):
        self.x = int(self.values[0], self.system)
        self.y = int(self.values[1], self.system)

    def __from_decimal(self, result):
        self.res = ''
        while result >= self.system:
            self.res += str(result % self.system)
            result //= self.system
        self.res += str(result % self.system)
        self.res = self.res[::-1]

    def process(self, operation: str = "+", values: tuple = ('0', '0'), system: int = 10) -> str:
        """
        :param operation: addition; division; multiplication; difference - all with icons
        :param values: operands tuple
        :param system: system of operands
        :return: operation over operands
        """
        self.system = system
        self.values = values
        self.__to_decimal()
        match operation:
            case "+":
                result = self.x + self.y
            case "-":
                result = self.x - self.y
            case "*":
                result = self.x * self.y
            case "/":
                result = self.x // self.y
            case _:
                if self.x % self.y != 0: raise Exception("fractional division, I pass")
                result = self.x // self.y
        self.__from_decimal(result)
        return self.res


if __name__ == "__main__":
    task1 = Task1()
    print(task1.process("+", ("11", "1"), 2))
