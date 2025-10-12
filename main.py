import time
import random
import streamlit as st
import matplotlib.pyplot as plt

from algorithms.bubble_sort import bubble_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.selection_sort import selection_sort
from algorithms.binary_search import binary_search

ALGOS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
}


def draw_state_fig(state, highlight=(), info=""):
    """Draws a bar chart with axis labels, title, and highlight indices."""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(9, 4))
    # If state is a grid (list of lists), flatten for now
    if not isinstance(state, (list, tuple)) or (len(state) and isinstance(state[0], (list, tuple))):
        # Fallback: show a simple text when non-list state
        ax.text(0.5, 0.5, str(state), ha='center', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        # colored bars with a subtle gradient and highlighted indices
        cmap = plt.get_cmap('Blues')
        n = len(state)
        colors = [cmap(0.3 + 0.7 * (i / max(1, n - 1))) for i in range(n)]
        bars = ax.bar(range(n), state, color=colors, edgecolor='black')
        if highlight:
            for idx in (highlight if isinstance(highlight, (list, tuple)) else [highlight]):
                if isinstance(idx, int) and 0 <= idx < len(bars):
                    bars[idx].set_color('#ff7f0e')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        ax.set_xticks(range(len(state)))
        ax.set_xlim(-0.5, max(len(state) - 0.5, 0.5))
        ax.set_ylim(0, max(state) * 1.1 if state else 1)
        # annotate bar values for clarity
        for rect, val in zip(bars, state):
            height = rect.get_height()
            ax.annotate(f'{val}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)
    ax.set_title(info, fontsize=12)
    plt.tight_layout()
    return fig


st.set_page_config(page_title="Algorithm Visualizer", layout="wide")
st.title("Algorithm Visualizer — Web Demo")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    algo_name = st.selectbox("Algorithm", list(ALGOS.keys()) + ["Binary Search"])
    st.markdown("**Array input (required)**")
    arr_text = st.text_input("Enter numbers separated by commas", "5,2,4,1,3")
    # Derive array strictly from user input (no randomization)
    try:
        arr = [int(x.strip()) for x in arr_text.split(",") if x.strip()!='']
    except Exception:
        st.error("Invalid array - use comma separated integers")
        arr = []
    # keep UI simple: array size is derived from number of inputs
    st.write(f"Array size: {len(arr)}")

    if algo_name == "Binary Search":
        target = st.number_input("Target value", value=arr[0] if arr else 0)

    # Speed control: base delay (ms) controls baseline speed; multiplier increases playback speed
    base_delay_ms = 160
    # persistent multiplier stored in session_state so changes persist across re-runs
    if 'multiplier' not in st.session_state:
        st.session_state.multiplier = 2

    col_a, col_b, col_c = st.columns([1,1,2])
    with col_a:
        if st.button("Speed -"):
            # halve the multiplier but keep at least 1
            st.session_state.multiplier = max(1, st.session_state.multiplier // 2)
    with col_b:
        if st.button("Speed +"):
            # double the multiplier each click (user requested "increase speed more, every time I select")
            st.session_state.multiplier = st.session_state.multiplier * 4
    with col_c:
        st.write("Current multiplier:", f"{st.session_state.multiplier}x")

    # provide a quick presets row for convenience
    preset_cols = st.columns([1,1,1,1])
    presets = [1,2,4,8]
    for pc, val in zip(preset_cols, presets):
        with pc:
            if st.button(f"{val}x"):
                st.session_state.multiplier = val
    multiplier = st.session_state.multiplier
    st.markdown("---")
    st.write("Playback")
    if 'playing' not in st.session_state:
        st.session_state.playing = False
    if 'frames' not in st.session_state:
        st.session_state.frames = []
    if 'idx' not in st.session_state:
        st.session_state.idx = 0

    if st.button("Generate frames"):
        # Build frames list from generator so we can step/play
        if not arr:
            st.warning("Provide a valid array first.")
            st.session_state.frames = []
        else:
            if algo_name == "Binary Search":
                st.session_state.frames = list(binary_search(sorted(arr), int(target)))
            else:
                st.session_state.frames = list(ALGOS[algo_name](arr))
        st.session_state.idx = 0
        st.session_state.playing = False

    # Clean play/pause/step buttons
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("Play ▶️"):
            st.session_state.playing = True
    with c2:
        if st.button("Pause ⏸️"):
            st.session_state.playing = False
    with c3:
        if st.button("Step ⏭️"):
            st.session_state.playing = False
            st.session_state.idx = min(st.session_state.idx + 1, max(len(st.session_state.frames) - 1, 0))

    if st.button("Reset"):
        st.session_state.idx = 0
        st.session_state.playing = False

    st.write("Current frame:", st.session_state.idx, "/", max(len(st.session_state.frames) - 1, 0))

# Main display
placeholder = st.empty()

def render_frame_at(i: int):
    if 0 <= i < len(st.session_state.frames):
        frame = st.session_state.frames[i]
        fig = draw_state_fig(frame.get('state', []), frame.get('highlight', ()), frame.get('info', ''))
        placeholder.pyplot(fig)
        plt.close(fig)

# If frames are present, show current frame
if st.session_state.frames:
    render_frame_at(st.session_state.idx)

# Playback loop (blocking): iterates frames while the playing flag is True.
# Note: this is a simple approach that does not support pausing mid-block reliably
# because Streamlit processes events between runs. It still provides Start/Stop/Step.
if st.session_state.playing and st.session_state.frames:
    # compute delay in seconds from base_delay_ms divided by multiplier
    delay = max(0.001, (base_delay_ms / max(1, multiplier)) / 1000.0)
    # iterate from current index
    for i in range(st.session_state.idx, len(st.session_state.frames)):
        # if playing was switched off via UI before starting this iteration, break
        if not st.session_state.playing:
            break
        render_frame_at(i)
        st.session_state.idx = i + 1
        time.sleep(delay)
    st.session_state.playing = False
    if st.session_state.idx >= len(st.session_state.frames):
        st.success("Done")

