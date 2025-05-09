import math


class Rational:
    def __init__(self, *args):
        if len(args) == 2:
            n, d = args
            if d == 0:
                raise ValueError("Invalid denominator")
        elif len(args) == 1 and isinstance(args[0], str):
            parts = args[0].split('/')
            if len(parts) != 2:
                raise ValueError("Invalid format")
            n, d = map(int, parts)
            if d == 0:
                raise ValueError("Invalid denominator")
        else:
            raise ValueError("Invalid arguments")

        common_divisor = math.gcd(abs(n), abs(d))
        self.n = n // common_divisor
        self.d = d // common_divisor

        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __str__(self):
        return f"{self.n}/{self.d}" if self.d != 1 else str(self.n)


class RationalList:
    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def __iter__(self):
        sorted_data = sorted(self.data, key=lambda x: (-x.d, -x.n))
        return iter(sorted_data)


def parse_file(input_filename):
    rationals = RationalList()
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                for part in line.strip().split():
                    try:
                        if '/' in part:
                            rationals.append(Rational(part))
                        else:
                            rationals.append(Rational(int(part), 1))
                    except (ValueError, TypeError):
                        continue
    except UnicodeDecodeError:
        # Спроба прочитати у іншому кодуванні, якщо UTF-8 не працює
        with open(input_filename, 'r', encoding='cp1251') as f:
            for line in f:
                for part in line.strip().split():
                    try:
                        if '/' in part:
                            rationals.append(Rational(part))
                        else:
                            rationals.append(Rational(int(part), 1))
                    except (ValueError, TypeError):
                        continue
    return rationals


def write_results(input_filename, rationals):
    output_filename = input_filename.replace('.txt', '_result.txt')
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("Дроби у порядку спадання знаменників:\n")
        f.write("------------------------------------\n")
        for num in rationals:
            f.write(f"{num}\n")
        f.write("\nУсього коректних дробів: " + str(len(rationals.data)))


def main():
    input_files = ['input01.txt', 'input02.txt', 'input03.txt']  # Ваші файли

    for filename in input_files:
        try:
            rationals = parse_file(filename)
            if not rationals.data:
                print(f"Файл {filename} не містить коректних дробів")
                continue

            write_results(filename, rationals)
            print(f"Успішно оброблено {filename}")
            print(f"Результати збережено у {filename.replace('.txt', '_result.txt')}")
            print(f"Знайдено коректних дробів: {len(rationals.data)}\n")
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено\n")


if __name__ == "__main__":
    main()