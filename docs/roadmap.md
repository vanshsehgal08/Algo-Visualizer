# Algorithm Visualizer — Project Roadmap & Contribution Guide

*Friendly guide by your pseudo-20s brilliant mentor: clear, a little sassy, and very practical.*  
This doc explains the whole idea, the simplified file structure, and every task broken into steps & substeps — from **first run** to **advanced features & maintainer checklist**. Use this as your contributor onboarding / maintainer playbook.

---

## 🚀 Project Summary (elevator pitch)

**Python Algorithm Visualizer** is a beginner-friendly repo where each algorithm (sorting, searching, pathfinding, etc.) is implemented in Python and exposes step-by-step state updates for visualization. Contributors add algorithms or new visualizations; maintainers merge PRs. The goal: many small, testable PRs that teach algorithm internals and look nice when animated.

---

## 🧩 Simplified File Structure (less nesting, same algorithm count)

Algorithm-Visualizer/
│
├── algorithms/ # All algorithm implementations (each file = one algo)
│ ├── bubble_sort.py
│ ├── insertion_sort.py
│ ├── selection_sort.py
│ ├── merge_sort.py
│ ├── quick_sort.py
│ ├── heap_sort.py
│ ├── binary_search.py
│ ├── bfs_pathfinding.py
│ └── ... # add more here (one file per algorithm)
│
├── visualizers/ # Visualizer entrypoints that render algorithm states
│ ├── sorting_visualizer.py
│ ├── searching_visualizer.py
│ └── pathfinding_visualizer.py
│
├── examples/ # Minimal runnable examples / demos
│ ├── run_sort_demo.py
│ └── run_path_demo.py
│
├── utils/
│ ├── draw_helpers.py # common draw functions (matplotlib wrappers)
│ └── algo_interface.py # interface helpers + utilities
│
├── tests/
│ └── test_algorithms.py
│
├── docs/
│ └── roadmap.md # this document
│
├── README.md
├── CONTRIBUTING.md
├── LICENSE
└── requirements.txt

🛠️ Basic — setup & first run (for maintainers and contributors)
Step 0 — Requirements

Python 3.8+ recommended

pip install -r requirements.txt (requirements should include matplotlib, numpy and pytest at minimum)

Step 1 — clone & install

Fork the repo → Clone → cd Algorithm-Visualizer

python -m venv .venv (optional) & source .venv/bin/activate or Windows equivalent

pip install -r requirements.txt

Step 2 — run a demo visualizer

python examples/run_sort_demo.py

This imports visualizers/sorting_visualizer.py which loads a sample dataset and uses the generator from an algorithm (e.g., bubble_sort).

If the window shows bars moving — success!

Step 3 — read code pattern

Open algorithms/bubble_sort.py — notice yield after swaps.

Open visualizers/sorting_visualizer.py — notice it consumes the generator and calls draw_helpers.draw_state(...).

✍️ Contributing: Add your first algorithm (detailed substeps)

This is the most important contributor flow — make PRs simple.

Goal:

Add a new algorithm file algorithms/<your_algo>.py that implements the interface and a short README example.

Substep A — Create the file

Create algorithms/<your_algo>.py

At the top, add a docstring: name, short description, complexity

Substep B — Implement algorithm as generator

Use the generator pattern: yield the state when a visible change happens (swap, compare, push/pop, path expansion).

Keep each yielded data_state as a simple list or matrix (serializable).

Metadata keys suggested:

highlight: indices to color

info: short string status (e.g., "swapped 2 & 3")

Substep C — Add tests

Add a small test to tests/test_algorithms.py:

Import your generator, collect yields on a short list, assert final state sorted.

Tests must be lightweight.

Substep D — Update docs

Add a one-line entry to docs/roadmap.md describing the new algorithm file and example command to run it.

Substep E — PR formatting

Title: Add: insertion_sort algorithm (generator interface)

Include: what you changed, how to run example, unit test results (optional)
done: boolean for final state
