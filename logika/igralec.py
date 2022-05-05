from enum import Enum

class Igralec(Enum):
    A = 0
    B = 1
    def nasprotnik(self):
        if self == Igralec.A:
            return Igralec.B
        else:
            return Igralec.A