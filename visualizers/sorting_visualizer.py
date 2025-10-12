"""Simple sorting visualizer that consumes sorting generators."""
import matplotlib.pyplot as plt
from typing import Callable, List
from utils.draw_helpers import draw_state


def visualize_sort(gen, initial_state: List[int]):
    plt.ion()
    fig = plt.figure()
    for frame in gen:
        draw_state(frame['state'], frame.get('highlight', ()), frame.get('info', ''))
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    # Quick manual demo
    from algorithms.bubble_sort import bubble_sort
    arr = [5, 3, 6, 2, 4, 1]
    visualize_sort(bubble_sort(arr), arr)
