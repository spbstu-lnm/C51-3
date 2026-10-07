#!/usr/bin/python

import argparse
import timeit
import itertools

from collections import deque


# extended euclidean algorithm, p.23
def egcd(a: int, b: int, log: bool = False) -> None:
    first_steps = deque(maxlen=20)
    last_steps = deque(maxlen=5)

    swapped = b > a
    if swapped:
        a, b = b, a

    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    i = 0
    while r1 != 0:
        q = r0 // r1
        i += 1

        r0, r1 = r1, (r0 - q * r1)

        x0, x1 = x1, (x0 - q * x1)
        y0, y1 = y1, (y0 - q * y1)

        if log:
            current_step = {'i': i, 'r': r0, 'x': x0, 'y': y0}
            if i <= 20:
                first_steps.append(current_step)
            last_steps.append(current_step)

    if swapped:
        x0, y0 = y0, x0

    if log:
        if i > 20:
            for v in itertools.islice(first_steps, 5):
                print(v)
            print("///   ///   ///")
            for v in last_steps:
                print(v)
        else:
            for v in first_steps:
                print(v)

        print(f"\n{i} --- ({a}, {b}) -> {r0} ({x0}, {y0})\n")


# extended binary euclidean algorithm, p.25
def ebgcd(a: int, b: int, log: bool = False) -> None:
    first_steps = deque(maxlen=20)
    last_steps = deque(maxlen=5)

    swapped = b > a
    if swapped:
        a, b = b, a

    ac, bc = a, b
    A, B, C, D = 1, 0, 0, 1

    g = 1
    while not (ac | bc) & 1:
        ac >>= 1
        bc >>= 1
        g <<= 1

    u, v = ac, bc

    i = 0
    while u:
        i += 1
        while not u & 1:
            u >>= 1
            if not (A | B) & 1:
                A >>= 1
                B >>= 1
            else:
                A = (A + bc) >> 1
                B = (B - ac) >> 1
        while not v & 1:
            v >>= 1
            if not (C | D) & 1:
                C >>= 1
                D >>= 1
            else:
                C = (C + bc) >> 1
                D = (D - ac) >> 1

        if u >= v:
            u -= v
            A -= C
            B -= D
        else:
            v -= u
            C -= A
            D -= B

        if log:
            current_step = {'i': i, 'r': g * v, 'x': C, 'y': D}
            if i <= 20:
                first_steps.append(current_step)
            last_steps.append(current_step)

    d = g * v
    x, y = C, D

    if swapped:
        x, y = y, x

    if log:
        if i > 20:
            for v in itertools.islice(first_steps, 5):
                print(v)
            print("///   ///   ///")
            for v in last_steps:
                print(v)
        else:
            for v in first_steps:
                print(v)

        print(f"\n{i} --- ({a}, {b}) -> {d} ({x}, {y})\n")
    

# extended trimmed euclidean algorithm
def etgcd(a: int, b: int, log: bool = False) -> None:
    first_steps = deque(maxlen=20)
    last_steps = deque(maxlen=5)
    
    swapped = b > a
    if swapped:
        a, b = b, a

    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    i = 0
    while r1 != 0:
        q = (r0 + r1 // 2) // r1
        i += 1

        r0, r1 = r1, (r0 - q * r1)

        x0, x1 = x1, (x0 - q * x1)
        y0, y1 = y1, (y0 - q * y1)

        if log:
            current_step = {'i': i, 'r': r0, 'x': x0, 'y': y0}
            if i <= 20:
                first_steps.append(current_step)
            last_steps.append(current_step)

    if r0 < 0:
        r0, x0, y0 = -r0, -x0, -y0

    if swapped:
        x0, y0 = y0, x0

    if log:
        if i > 20:
            for v in itertools.islice(first_steps, 5):
                print(v)
            print("///   ///   ///")
            for v in last_steps:
                print(v)
        else:
            for v in first_steps:
                print(v)

        print(f"\n{i} --- ({a}, {b}) -> {r0} ({x0}, {y0})\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("a", help="first number", type=int)
    parser.add_argument("b", help="second number", type=int)

    parser.add_argument("-b", "--benchmark", dest="benchmark",
                        help="measure algorithm execution time", 
                        action="store_true")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.benchmark:
        ITERS = 100000

        print(timeit.timeit(lambda: egcd(args.a, args.b), number=ITERS) / ITERS)
        print(timeit.timeit(lambda: ebgcd(args.a, args.b), number=ITERS) / ITERS)
        print(timeit.timeit(lambda: etgcd(args.a, args.b), number=ITERS) / ITERS)
    else:
        egcd(args.a, args.b, True)
        ebgcd(args.a, args.b, True)
        etgcd(args.a, args.b, True)


if __name__ == '__main__':
    main()
