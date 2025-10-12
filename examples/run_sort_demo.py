"""Run a small sorting demo using bubble sort visualizer."""
from visualizers.sorting_visualizer import visualize_sort
from algorithms.bubble_sort import bubble_sort


def main():
    arr = [5, 2, 4, 1, 3]
    visualize_sort(bubble_sort(arr), arr)


if __name__ == '__main__':
    main()
