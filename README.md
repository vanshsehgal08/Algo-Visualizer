# Algorithm Visualizer

Minimal, extensible Python Algorithm Visualizer with small demos and a Streamlit web UI.

This repository contains simple algorithm implementations (sorting, search, pathfinding) plus small visualizers and example scripts you can run locally. It's designed for learning, teaching, and quick experimentation.

Features

- Lightweight algorithm implementations with generator-based frame output for visualization.
- Streamlit-based web demo (`web_app.py`) for interactive playback and stepping through frames.
- Example CLI/demo scripts under `examples/`.
- Small test suite for core algorithms.

Requirements

- Python 3.8+
- See `requirements.txt` for the exact pinned dependencies (recommended to use a virtualenv).

Quick start (recommended)

1. Create and activate a virtualenv:

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```pwsh
pip install -r requirements.txt
```

Run the Streamlit visualizer

1. Start the web demo (opens in your browser):

```pwsh
streamlit run d:\Algo-Visualizer\web_app.py
```

2. In the sidebar you can:

- Choose an algorithm (Bubble Sort, Insertion Sort, Selection Sort, Binary Search).
- Enter an array as comma-separated integers (e.g. `5,2,4,1,3`).
- Generate frames and use Play / Pause / Step controls to inspect the algorithm.
- Adjust playback speed using the Speed + / Speed - buttons and presets (multiplier persists across runs).

Run the example sorting demo (non-Streamlit)

```pwsh
python examples/run_sort_demo.py
```

Algorithms included

- Sorting
  - `bubble_sort` — stable O(n^2) algorithm, implemented with generator frames for visualization.
  - `insertion_sort` — simple O(n^2) algorithm, generator-based frames.
  - `selection_sort` — O(n^2) selection-based sort.
- Searching
  - `binary_search` — generator-based binary search that yields frames showing the current range and highlight.
- Pathfinding (example)
  - `bfs_pathfinding` — breadth-first search demo for grid/path visualizations.

Project layout (important files)

- `web_app.py` — Streamlit UI and visualization playback logic.
- `algorithms/` — algorithm implementations that yield frames as dicts with `state`, `highlight`, and `info` keys.
- `visualizers/` — helper visualizers (sorting_visualizer, etc.).
- `examples/` — small example scripts such as `run_sort_demo.py`.
- `tests/` — unit tests for algorithms.
- `docs/roadmap.md` — contributor guide and roadmap.

Development notes

- Each algorithm yields frames as dictionaries. A typical frame looks like:

```py
{
		'state': [5, 2, 4, 1, 3],
		'highlight': (i, j),  # indices to highlight in the UI
		'info': 'Comparing index i and j',
}
```

- The Streamlit UI (`web_app.py`) consumes those frames and renders them as bar charts. Playback speed is controlled by a `multiplier` stored in `st.session_state`.

Testing

- Run the test suite with:

```pwsh
python -m pytest -q
```

Contributing

- Please read `docs/roadmap.md` for contribution guidelines and roadmap details.
- To add a new algorithm:
  1.  Add the implementation under `algorithms/` and make it yield frames like other algorithms.
  2.  Add a small unit test under `tests/` and update `visualizers/` if a custom renderer is needed.
  3.  Open a PR with a descriptive title and test coverage for new behavior.

License

- This project is open source; see the `LICENSE` file for details.

Contact / Questions

- If you want help adding an algorithm or improving the UI, open an issue or PR and I'll help review.

Enjoy exploring algorithms!
