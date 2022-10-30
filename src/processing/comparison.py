class Comparison:
    def compare(self, a, b):
        return False

class Equals(Comparison):
    def compare(self, a, b):
        return a == b

class GreaterThan(Comparison):
    def compare(self, a, b):
        return a > b

class LessThan(Comparison):
    def compare(self, a, b):
        return a < b

class Contains(Comparison):
    def compare(self, a: str, b):
        return a.__contains__(b)
