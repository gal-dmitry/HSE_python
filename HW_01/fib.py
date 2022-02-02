from math import sqrt


def fib(n):
    phi = (1 + sqrt(5)) / 2
    return int((phi**n - (-phi)**(-n)) / (2*phi - 1))