import time
from multiprocessing import Process
from threading import Thread


def fib(n):
    if n < 0:
        raise ValueError(f"n < 0")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def run(n, times, executor=None):
    if executor is None:
        [fib(n) for _ in range(times)]
    else:
        executors = [executor(target=fib, args=(n,)) for _ in range(times)]
        [ex.start() for ex in executors]
        [ex.join() for ex in executors]


def eval_time(n, times, executor=None):
    start_time = time.time()
    run(n, times, executor=executor)
    return time.time() - start_time


def main():

    n, times = 35, 10

    with open("artefacts/easy.txt", "w") as file:

        file.write(f"Args: n={n}, times={times}\n")
        file.write("\n")

        print("Base run ...")
        file.write(f"Base run: {eval_time(n, times):.2f} sec\n")

        print("Threading run ...")
        file.write(f"Threading run: {eval_time(n, times, executor=Thread):.2f} sec\n")

        print("Multiprocessing run ...")
        file.write(f"Multiprocessing run: {eval_time(n, times, executor=Process):.2f} sec\n")


if __name__ == "__main__":
    main()