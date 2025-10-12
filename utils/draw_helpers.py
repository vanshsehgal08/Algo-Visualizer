"""Minimal drawing helpers using matplotlib."""
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt


def draw_state(state: List[int], highlight=(), info: str = ""):
    plt.clf()
    bars = plt.bar(range(len(state)), state, color=['C0']*len(state))
    if highlight:
        for idx in (highlight if isinstance(highlight, (list, tuple)) else [highlight]):
            if 0 <= idx < len(bars):
                bars[idx].set_color('C1')
    plt.title(info)
    plt.pause(0.05)
