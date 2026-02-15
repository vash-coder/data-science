import timeit
import random
from collections import Counter


NUMBERS = [random.randint(0, 100) for _ in range(1_000_000)]

def my_counter(numbers):
    result = {}
    for number in numbers:
        if number in result:
            result[number] += 1
        else:
            result[number] = 1
    return result

def counter_numbers(numbers):
    return Counter(numbers)

def my_top(numbers):
    counts = my_counter(numbers)
    sorted_list = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_list[:10])

def counter_top(numbers):
    return dict(Counter(numbers).most_common(10))

def main():
    time_my_counter = timeit.timeit(lambda: my_counter(NUMBERS), number=1)
    time_counter = timeit.timeit(lambda: counter_numbers(NUMBERS), number=1)
    time_my_top = timeit.timeit(lambda: my_top(NUMBERS), number=1)
    time_counter_top = timeit.timeit(lambda: counter_top(NUMBERS), number=1)

    print(f"my function: {time_my_counter}")
    print(f"Counter: {time_counter}")
    print(f"my top: {time_my_top}")
    print(f"Counter's top: {time_counter_top}")

if __name__ == '__main__':
    main()