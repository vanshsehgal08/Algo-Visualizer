"""Common interface helpers for algorithms"""
from typing import Callable, Any


def collect_generator(gen):
    """Collect yields from a generator into a list and return final result when available."""
    frames = []
    result = None
    for item in gen:
        frames.append(item)
    return frames
