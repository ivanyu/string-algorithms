#!/usr/bin/env python
# -*- coding: utf-8 -*-


def z_naive(s):
    """The naive computation of Z-values of a string."""

    Z = [len(s)]

    for k in range(1, len(s)):
        n = 0
        while n + k < len(s) and s[n] == s[n + k]:
            n += 1
        Z.append(n)

    return Z


def z_advanced(s):
    """An advanced computation of Z-values of a string."""

    Z = [0] * len(s)
    Z[0] = len(s)

    rt = 0
    lt = 0

    for k in range(1, len(s)):
        if k > rt:
            # If k is outside the current Z-box, do naive computation.
            n = 0
            while n + k < len(s) and s[n] == s[n+k]:
                n += 1
            Z[k] = n
            if n > 0:
                lt = k
                rt = k+n-1
        else:
            # If k is inside the current Z-box, consider two cases.

            p = k - lt  # Pair index.
            right_part_len = rt - k + 1

            if Z[p] < right_part_len:
                Z[k] = Z[p]
            else:
                i = rt + 1
                while i < len(s) and s[i] == s[i - k]:
                    i += 1
                Z[k] = i - k

                lt = k
                rt = i - 1
    return Z


def search(pattern, text):
    """Search with the sentinel."""

    result = []

    zs = z_advanced('{0}${1}'.format(pattern, text))
    for i, z in enumerate(zs):
        if z == len(pattern):
            result.append(i - len(pattern) - 1)

    return result


def search_without_sentinel(pattern, text):
    """Search without the sentinel."""

    # The algorithm is z_advanced with restriction of possible Z-values to the
    # length of the pattern.
    # During the computation, all equalities of an Z-value and the length of
    # the pattern are noted - these are occurrence.

    s = pattern + text
    Z = [0] * len(s)
    Z[0] = len(s)

    rt = 0
    lt = 0

    occurrence = []

    for k in range(1, len(s)):
        if k > rt:
            n = 0
            while n + k < len(s) and s[n] == s[n+k]:
                n += 1
            Z[k] = n
            if n > 0:
                lt = k
                rt = k+n-1
        else:
            p = k - lt
            right_part_len = rt - k + 1

            if Z[p] < right_part_len:
                Z[k] = Z[p]
            else:
                i = rt + 1
                while i < len(s) and s[i] == s[i - k]:
                    i += 1
                Z[k] = i - k

                lt = k
                rt = i - 1

        Z[k] = min(len(pattern), Z[k])

        # An occurence found.
        if Z[k] == len(pattern):
            occurrence.append(k - len(pattern))

    return occurrence


if __name__ == "__main__":
    import random
    from time import time

    # Random tests.
    r = random.Random()
    r.seed(time())
    src = [str(i) for i in range(10)]
    for i in range(1, 40000):
        s = ''.join([r.choice(src) for _ in range(r.randint(1, 400))])
        try:
            assert(z_naive(s) == z_advanced(s))
        except Exception:
            print(s)
            raise
