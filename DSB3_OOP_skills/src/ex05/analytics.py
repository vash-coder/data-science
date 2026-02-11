from random import randint


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self, has_header=True):
        try:
            with open(self.path, "r") as file:
                lines = file.read().strip().split("\n")
        except Exception as e:
            raise Exception(f"Cannot read file: {e}")

        if not self.check_structure(lines):
            raise Exception("Invalid file structure")

        if has_header:
            lines = lines[1:]

        data = []
        for line in lines:
            data.append([int(x) for x in line.split(",")])

        return data

    def check_structure(self, lines):
        if len(lines) < 2:
            return False

        if lines[0] != "head,tail":
            return False

        for line in lines[1:]:
            if line not in ["0,1", "1,0"]:
                return False

        return True

class Calculations:
    def __init__(self, data):
        self.data = data

    def counts(self):
        heads = 0
        tails = 0
        for item in self.data:
            if item == [1, 0]:
                heads += 1
            elif item == [0, 1]:
                tails += 1
        return heads, tails

    def fractions(self):
        heads, tails = self.counts()
        total = heads + tails
        return round(heads / total, 4), round(tails / total, 4)

class Analytics(Calculations):
    def predict_random(self, n):
        result = []
        for _ in range(n):
            r = randint(0, 1)
            if r == 1:
                result.append([1, 0])
            else:
                result.append([0, 1])
        return result

    def predict_last(self):
        return self.data[-1]

    def save_file(self, data, filename, extension):
        with open(f"{filename}.{extension}", "w") as file:
            file.write(data)