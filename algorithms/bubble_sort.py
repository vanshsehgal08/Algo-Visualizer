"""Bubble Sort (generator)

Yields dicts with:
- state: list of numbers
- highlight: tuple of indices being compared or swapped
- info: short string
"""
from typing import List, Generator, Dict


def bubble_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    n = len(a)
    yield {"state": a.copy(), "highlight": (), "info": "start"}
    for i in range(n):
        for j in range(0, n - i - 1):
            yield {"state": a.copy(), "highlight": (j, j + 1), "info": f"compare {j} and {j+1}"}
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                yield {"state": a.copy(), "highlight": (j, j + 1), "info": f"swapped {j} & {j+1}"}
    yield {"state": a.copy(), "highlight": (), "info": "done"}
