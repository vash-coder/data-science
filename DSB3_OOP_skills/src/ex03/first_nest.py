import sys


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        try:
            with open(self.path, "r") as file:
                content = file.read()
        except Exception as e:
            raise Exception(f"Cannot read file: {e}")

        lines = [line.strip() for line in content.strip().split("\n") if line.strip() != ""]

        if not self.check_structure(lines, has_header):
            raise Exception(f"Invalid file structure")

        if has_header:
            lines = lines[1:]

        return [self.to_list(line) for line in lines]

    def check_structure(self, lines, has_header):
        if has_header:
            if len(lines) < 2:
                return False
            if lines[0].strip() != "head,tail":
                return False
        else:
            if len(lines) < 1:
                return False

        data_lines = lines[1:] if has_header else lines
        for line in data_lines:
            if line.strip() not in ["0,1", "1,0"]:
                return False
        return True

    def to_list(self, line: str):
        if line == "1,0":
            return [1, 0]
        elif line == "0,1":
            return [0, 1]
        raise Exception(f"Invalid line content: {line}")

    class Calculations:
        def counts(self, data):
            heads = sum(1 for item in data if item == [1, 0])
            tails = sum(1 for item in data if item == [0, 1])
            return heads, tails

        def fractions(self, heads, tails):
            total = heads + tails
            return round(heads / total, 4), round(tails / total, 4)

def main():
    if len(sys.argv) not in [2, 3]:
        raise Exception("Invalid number of arguments")

    path = sys.argv[1]

    has_header = sys.argv[2] == "True" if len(sys.argv) == 3 else True

    research = Research(path)
    data = research.file_reader(has_header)

    calculations = Research.Calculations()
    heads, tails = calculations.counts(data)
    fractions = calculations.fractions(heads, tails)

    print(data)
    print(heads, tails)
    print(fractions[0], fractions[1])


if __name__ == "__main__":
    main()