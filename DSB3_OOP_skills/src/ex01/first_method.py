class Research:
    def file_reader(self):
        try:
            with open("data.csv", "r") as file:
                return file.read()
        except Exception as e:
            return e


def main():
    print(Research().file_reader())


if __name__ == '__main__':
    main()