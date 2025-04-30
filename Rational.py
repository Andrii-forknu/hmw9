from math import gcd

class Rational:
    def __init__(self, numerator, denominator=None):
        if denominator is not None:
            self.numerator = int(numerator)
            self.denominator = int(denominator)
        else:
            if isinstance(numerator, str):
                parts = numerator.strip().split('/')
                if len(parts) != 2:
                    raise ValueError("Invalid string format, expected 'n/d'")
                self.numerator = int(parts[0])
                self.denominator = int(parts[1])
            elif isinstance(numerator, Rational):
                self.numerator = numerator.numerator
                self.denominator = numerator.denominator
            else:
                raise TypeError("Invalid argument type")

        if self.denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")

        self._reduce()

    def _reduce(self):
        common = gcd(self.numerator, self.denominator)
        self.numerator //= common
        self.denominator //= common
        # Keep denominator positive
        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def __add__(self, other):
        other = Rational(other, 1) if isinstance(other, int) else other
        if not isinstance(other, Rational):
            raise TypeError("Operand must be Rational or int")
        num = self.numerator * other.denominator + other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Rational(num, den)

    def __sub__(self, other):
        other = Rational(other, 1) if isinstance(other, int) else other
        if not isinstance(other, Rational):
            raise TypeError("Operand must be Rational or int")
        num = self.numerator * other.denominator - other.numerator * self.denominator
        den = self.denominator * other.denominator
        return Rational(num, den)

    def __mul__(self, other):
        other = Rational(other, 1) if isinstance(other, int) else other
        if not isinstance(other, Rational):
            raise TypeError("Operand must be Rational or int")
        return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        other = Rational(other, 1) if isinstance(other, int) else other
        if not isinstance(other, Rational):
            raise TypeError("Operand must be Rational or int")
        if other.numerator == 0:
            raise ZeroDivisionError("Division by zero")
        return Rational(self.numerator * other.denominator, self.denominator * other.numerator)

    def __call__(self):
        return self.numerator / self.denominator

    def __getitem__(self, key):
        if key == "n":
            return self.numerator
        elif key == "d":
            return self.denominator
        else:
            raise KeyError("Use 'n' for numerator or 'd' for denominator")

    def __setitem__(self, key, value):
        if key == "n":
            self.numerator = int(value)
        elif key == "d":
            if int(value) == 0:
                raise ZeroDivisionError("Denominator cannot be zero")
            self.denominator = int(value)
        else:
            raise KeyError("Use 'n' for numerator or 'd' for denominator")
        self._reduce()
class RationalList:
    def __init__(self, initial=None):
        self.data = []
        if initial is not None:
            for item in initial:
                self._append_valid(item)

    def _append_valid(self, item):
        if isinstance(item, Rational):
            self.data.append(item)
        elif isinstance(item, int):
            self.data.append(Rational(item, 1))
        else:
            raise TypeError("Only Rational or int types are allowed in RationalList")

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(value, Rational):
            self.data[index] = value
        elif isinstance(value, int):
            self.data[index] = Rational(value, 1)
        else:
            raise TypeError("Only Rational or int can be assigned to RationalList")

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        new_list = RationalList(self.data)
        if isinstance(other, RationalList):
            for item in other.data:
                new_list._append_valid(item)
        elif isinstance(other, Rational) or isinstance(other, int):
            new_list._append_valid(other)
        else:
            raise TypeError("Can only add RationalList, Rational, or int to RationalList")
        return new_list

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            for item in other.data:
                self._append_valid(item)
        elif isinstance(other, Rational) or isinstance(other, int):
            self._append_valid(other)
        else:
            raise TypeError("Can only add RationalList, Rational, or int to RationalList")
        return self

    def sum(self):
        result = Rational(0, 1)
        for item in self.data:
            result += item
        return result

def parse_token(token):
    if '/' in token:
        return Rational(token)
    else:
        return Rational(int(token), 1)

def evaluate_expression_with_precedence(expression):
    tokens = expression.strip().split()
    if not tokens:
        return None

    # Крок 1: обробка множення і ділення
    intermediate = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ('*', '/'):
            prev = intermediate.pop()
            next_val = parse_token(tokens[i + 1])
            prev_val = parse_token(prev) if isinstance(prev, str) else prev
            if token == '*':
                result = prev_val * next_val
            else:
                result = prev_val / next_val
            intermediate.append(result)
            i += 2
        else:
            intermediate.append(token)
            i += 1

    # Крок 2: обробка додавання і віднімання
    result = parse_token(intermediate[0]) if isinstance(intermediate[0], str) else intermediate[0]
    i = 1
    while i < len(intermediate):
        op = intermediate[i]
        next_val = intermediate[i + 1]
        next_val = parse_token(next_val) if isinstance(next_val, str) else next_val
        if op == '+':
            result = result + next_val
        elif op == '-':
            result = result - next_val
        i += 2
    return result
def parse_rational_or_int(token):
    token = token.strip()
    if '/' in token:
        return Rational(token)
    else:
        return Rational(int(token), 1)

def process_file(filename):
    rlist = RationalList()
    with open(filename, "r") as file:
        for line in file:
            tokens = line.strip().split()
            for token in tokens:
                if token:
                    rlist += parse_rational_or_int(token)
    return rlist



with open("input01.txt", "r") as file:
    for line_num, line in enumerate(file, 1):
        try:
            result = evaluate_expression_with_precedence(line)
            print(f"Рядок {line_num}: {result} = {result()}")
        except Exception as e:
            print(f"Рядок {line_num}: Помилка – {e}")
for fname in ["input04.txt", "input02.txt", "input03.txt"]:
    try:
        rlist = process_file(fname)
        total = rlist.sum()
        print(f"Файл {fname}: сума = {total} = {total()}")
    except Exception as e:
        print(f"Файл {fname}: Помилка – {e}")

