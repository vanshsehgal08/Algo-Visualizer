"""Breadth-First Search pathfinding generator for grid.
Yields expansions as sets of visited coordinates and current frontier.
"""
from typing import List, Tuple, Generator, Dict
from collections import deque


def bfs_pathfinding(grid: List[List[int]], start: Tuple[int, int], goal: Tuple[int, int]) -> Generator[Dict, None, None]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    visited = set()
    q = deque()
    q.append((start, [start]))
    visited.add(start)
    yield {"state": grid, "highlight": [start], "info": "start"}
    while q:
        (r, c), path = q.popleft()
        yield {"state": grid, "highlight": path, "info": f"visit {r},{c}"}
        if (r, c) == goal:
            yield {"state": grid, "highlight": path, "info": "goal"}
            return
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append(((nr, nc), path+[(nr, nc)]))
    yield {"state": grid, "highlight": [], "info": "not found"}
