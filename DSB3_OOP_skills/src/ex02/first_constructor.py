import sys


class Research:
    def __init__(self, path):
        self.path = path

    def file_reader(self):
        try:
            with open(self.path, "r") as file:
                content = file.read()
        except Exception as e:
            raise Exception(f"Cannot read file: {e}")

        if self.check_structure(content):
            return content
        else:
            raise Exception("Invalid file structure")

    def check_structure(self, content):
        lines = content.split("\n")

        if len(lines) < 2:
            return False

        if lines[0] != "head,tail":
            return False

        for line in lines[1:]:
            if line not in ["0,1", "1,0"]:
                return False

        return True


def main():
    if len(sys.argv) != 2:
        raise Exception("Invalid number of arguments")

    path = sys.argv[1]
    research = Research(path)
    print(research.file_reader())


if __name__ == "__main__":
    main()