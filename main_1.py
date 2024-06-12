class Fraction:
    @staticmethod
    def gcd(a,b):
        a = abs(a)
        b = abs(b)

        while b != 0:
            a , b = b, a % b
        return a




    def __init__(self, numerator, denominator):
        d = Fraction.gcd(numerator, denominator)
        assert denominator != 0
        self.numerator = (1 if denominator > 0 else -1) * (numerator//d)
        self.denominator = abs(denominator)//d

    def __str__(self):
        return f" {self.numerator}/{self.denominator} "
    def __repr__(self):
        return f"{type(self).__name__}({self.numerator!r}, {self.denominator!r})"

    def __getitem__(self, item):
        if item == 0:
            return self.numerator
        elif item ==1:
            return self.denominator
        else:
            raise IndexError
    def __init__(self):
        return self[0]//self[1]



f = Fraction(12, 15)
print(f)


fffff

