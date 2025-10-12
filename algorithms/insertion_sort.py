"""Insertion Sort (generator)
"""
from typing import List, Generator, Dict


def insertion_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    yield {"state": a.copy(), "highlight": (), "info": "start"}
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        yield {"state": a.copy(), "highlight": (i,), "info": f"take {i}"}
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            yield {"state": a.copy(), "highlight": (j + 1,), "info": "shift"}
        a[j + 1] = key
        yield {"state": a.copy(), "highlight": (j + 1,), "info": f"placed at {j+1}"}
    yield {"state": a.copy(), "highlight": (), "info": "done"}
