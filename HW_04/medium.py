import os
import logging
import math

from timeit import timeit
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def get_logger(filename):
    logging.basicConfig(filename=filename, level=logging.INFO, format="%(asctime)s | %(message)s")
    return logging.getLogger(os.path.basename(__file__))


def sync_integrate(f, a, b, *, n_iter=1000, logger=None):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        logger.info(f"Sync process: x = {i}")
        acc += f(a + i * step) * step
    return acc


def partial_integrate(args):
    f, a, i, step, logger = args
    x = a + i * step
    logger.info(f"Parallel process: x = {x}")
    return f(x)


def parallel_integrate(f, a, b, executor, *, n_jobs=1, n_iter=1000, logger=None):
    step = (b - a) / n_iter
    with executor(max_workers=n_jobs) as t:
        parts = list(t.map(partial_integrate, [(f, a, i, step, logger) for i in range(n_iter)]))
    return sum(parts) * step


if __name__ == "__main__":

    logger = get_logger("artefacts/medium_log.txt")
    n_iter = 1_000
    # n_iter = 10
    n_jobs_range = list(range(1, 2 * os.cpu_count() + 1))
    thread_time = []
    process_time = []

    ### Sync
    sync_time = timeit(lambda: sync_integrate(math.cos, 0, math.pi / 2, n_iter=n_iter, logger=logger), number=1)
    logger.info(f" --- ")

    ### Thread
    for n_jobs in n_jobs_range:
        time = timeit(lambda: parallel_integrate(math.cos,
                                                0,
                                                math.pi / 2,
                                                ThreadPoolExecutor,
                                                n_jobs=n_jobs,
                                                n_iter=n_iter,
                                                logger=logger), number=1)
        thread_time.append(time)

    logger.info(f" --- ")

    ### Multi
    for n_jobs in n_jobs_range:
        time = timeit(lambda: parallel_integrate(math.cos,
                                                0,
                                                math.pi / 2,
                                                ProcessPoolExecutor,
                                                n_jobs=n_jobs,
                                                n_iter=n_iter,
                                                logger=logger), number=1)
        process_time.append(time)

    logger.info(f" --- ")

    with open("artefacts/medium_compare.csv", "w") as f:
        f.write("n_jobs, Sync, Thread, Process\n")
        for n_jobs, thread_t, process_t in zip(n_jobs_range, thread_time, process_time):
            f.write(f"{n_jobs}, {sync_time}, {thread_t}, {process_t}\n")
