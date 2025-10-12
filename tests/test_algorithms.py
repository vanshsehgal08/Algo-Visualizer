import unittest
from algorithms.bubble_sort import bubble_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.selection_sort import selection_sort
from algorithms.binary_search import binary_search


class TestAlgorithms(unittest.TestCase):
    def test_bubble_sort(self):
        arr = [3,1,2]
        frames = list(bubble_sort(arr))
        self.assertEqual(frames[-1]['state'], [1,2,3])

    def test_insertion_sort(self):
        arr = [4,2,3,1]
        frames = list(insertion_sort(arr))
        self.assertEqual(frames[-1]['state'], [1,2,3,4])

    def test_selection_sort(self):
        arr = [2,5,1]
        frames = list(selection_sort(arr))
        self.assertEqual(frames[-1]['state'], [1,2,5])

    def test_binary_search_found(self):
        arr = [1,2,3,4,5]
        gen = binary_search(arr, 3)
        frames = list(gen)
        # last 'found' frame has info 'found'
        self.assertTrue(any(f['info']=='found' for f in frames))


if __name__ == '__main__':
    unittest.main()
