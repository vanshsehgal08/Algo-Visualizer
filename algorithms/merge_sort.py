"""Merge Sort (generator)
"""
from typing import List, Generator, Dict


def merge_sort(arr: List[int]) -> Generator[Dict, None, None]:
    a = arr.copy()
    yield from _merge_sort(a, 0, len(a) - 1)


def _merge_sort(a: List[int], left: int, right: int) -> Generator[Dict, None, None]:
    if left >= right:
        return

    mid = (left + right) // 2
    yield from _merge_sort(a, left, mid)
    yield from _merge_sort(a, mid + 1, right)
    yield from _merge(a, left, mid, right)
    yield {"state": a.copy(), "highlight": (), "info": f"merged {left}-{right}"}


def _merge(a: List[int], left: int, mid: int, right: int) -> Generator[Dict, None, None]:
    merged = []
    i, j = left, mid + 1

    while i <= mid and j <= right:
        yield {"state": a.copy(), "highlight": (i, j), "info": f"compare {i} and {j}"}
        if a[i] <= a[j]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(a[j])
            j += 1

    while i <= mid:
        merged.append(a[i])
        i += 1

    while j <= right:
        merged.append(a[j])
        j += 1

    for idx, val in enumerate(merged):
        a[left + idx] = val
        yield {"state": a.copy(), "highlight": (left + idx,), "info": f"inserted {val} at {left + idx}"}
