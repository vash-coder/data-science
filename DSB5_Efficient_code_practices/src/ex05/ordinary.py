import sys
import os
import psutil


def read_lines(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.readlines()


def main():
    if len(sys.argv) != 2:
        raise Exception("Please input the path of the file")

    path = sys.argv[1]
    p = psutil.Process(os.getpid())

    start_cpu = p.cpu_times()

    lines = read_lines(path)
    for _ in lines:
        pass

    end_cpu = p.cpu_times()

    mem = p.memory_info()
    peak_memory = getattr(mem, 'peak_wset', mem.rss) / (1024 ** 3)

    cpu_time = (end_cpu.user + end_cpu.system) - \
               (start_cpu.user + start_cpu.system)

    print(f"Peak Memory Usage = {peak_memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")


if __name__ == "__main__":
    main()
