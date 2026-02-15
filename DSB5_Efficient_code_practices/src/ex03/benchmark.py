import timeit
import sys
from functools import reduce


def square_loop(number):
    total = 0
    for i in range(1, number + 1):
        total += i * i
    return total


def square_reduce(number):
    return reduce(lambda acc, x: acc + x * x, range(1, number + 1), 0)


FUNCTIONS = {
    'loop': square_loop,
    'reduce': square_reduce
}


def main():
    if len(sys.argv) != 4:
        raise Exception("Incorrect number of arguments")

    function_name = sys.argv[1]
    try:
        calls = int(sys.argv[2])
        number = int(sys.argv[3])
    except ValueError:
        raise Exception("Incorrect number of arguments")

    if function_name not in FUNCTIONS:
        raise Exception(f"Function {function_name} does not exist")

    function = FUNCTIONS[function_name]

    time = timeit.timeit(lambda: function(number), number=calls)
    print(time)


if __name__ == '__main__':
    main()