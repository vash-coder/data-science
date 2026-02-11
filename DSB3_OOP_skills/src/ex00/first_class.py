class Must_read:
    def __init__(self):
        try:
            with open("data.csv", "r") as file:
                print(file.read())
        except FileNotFoundError as e:
            print(e)


if __name__ == "__main__":
    Must_read()