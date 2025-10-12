"""Selection Sort (generator)
"""
from typing import List, Generator, Dict


def selection_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    n = len(a)
    yield {"state": a.copy(), "highlight": (), "info": "start"}
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield {"state": a.copy(), "highlight": (min_idx, j), "info": f"compare {min_idx} and {j}"}
            if a[j] < a[min_idx]:
                min_idx = j
                yield {"state": a.copy(), "highlight": (min_idx,), "info": f"new min {min_idx}"}
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            yield {"state": a.copy(), "highlight": (i, min_idx), "info": f"swapped {i} & {min_idx}"}
    yield {"state": a.copy(), "highlight": (), "info": "done"}
