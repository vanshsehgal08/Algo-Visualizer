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

ALGO_DESCRIPTIONS = {
    "": "",
    
}


def draw_state_fig(state, highlight=(), info=""):
    """Draws a bar chart with axis labels, title, and highlight indices."""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 3))
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
    # Title removed to avoid duplicating the action description (shown in bottom bar)
    plt.tight_layout()
    return fig


st.set_page_config(page_title="Algorithm Visualizer", layout="wide")
if 'algo_name' not in st.session_state:
    st.session_state.algo_name = "Bubble Sort"
st.title(f"Algorithm Visualizer — {st.session_state.algo_name}")

# UI state defaults
if 'setup_visible' not in st.session_state:
    st.session_state.setup_visible = True
if 'arr_text' not in st.session_state:
    st.session_state.arr_text = "5,2,4,1,3"
if 'rand_size' not in st.session_state:
    st.session_state.rand_size = 10
if 'rand_seed' not in st.session_state:
    # fixed seed per session for stability of random previews unless size changes
    st.session_state.rand_seed = int(time.time())
if 'rand_array' not in st.session_state:
    st.session_state.rand_array = []
if 'playing' not in st.session_state:
    st.session_state.playing = False
if 'frames' not in st.session_state:
    st.session_state.frames = []
if 'idx' not in st.session_state:
    st.session_state.idx = 0
if 'speed_mult' not in st.session_state:
    st.session_state.speed_mult = 1.0

## Removed top hide/show toggle to keep layout stable

# Sidebar controls (Setup Panel)
with st.sidebar:
    with st.expander("Setup Panel", expanded=st.session_state.setup_visible):
        # Form for setup and visualization trigger
        with st.form("visualization_form"):
            algo_name = st.selectbox("Algorithm", list(ALGOS.keys()) + ["Binary Search"])
            st.session_state.algo_name = algo_name

            st.markdown("**Data Input**")
            tabs = st.tabs(["Manual Input", "Generate Random"]) 
            with tabs[0]:
                st.session_state.arr_text = st.text_area(
                    "Enter comma-separated values",
                    st.session_state.arr_text,
                    height=80,
                    key="manual_arr_text",
                )
            with tabs[1]:
                size = st.slider("Array Size", min_value=2, max_value=50, value=st.session_state.rand_size, key="rand_size_slider")
                # Regenerate preview array only when size changes
                if size != st.session_state.rand_size or not st.session_state.rand_array:
                    import random as _r
                    rng = _r.Random(st.session_state.rand_seed)
                    st.session_state.rand_array = [rng.randint(1, 99) for _ in range(size)]
                    st.session_state.rand_size = size
                # Show and bind to arr_text
                preview = ",".join(map(str, st.session_state.rand_array))
                st.session_state.arr_text = preview
                st.code(preview)

            if algo_name == "Binary Search":
                target = st.number_input("Target value", value=5)

            # Primary action at bottom
            visualize_submit = st.form_submit_button("Visualize", use_container_width=True, type="primary")

            if visualize_submit:
                try:
                    arr = [int(x.strip()) for x in st.session_state.arr_text.split(",") if x.strip()!='']
                    if not arr:
                        st.error("Please enter at least one number")
                    else:
                        if algo_name == "Binary Search":
                            st.session_state.frames = list(binary_search(sorted(arr), int(target)))
                        else:
                            st.session_state.frames = list(ALGOS[algo_name](arr))
                        st.session_state.idx = 0
                        st.session_state.playing = False
                        st.success(f"Generated {len(st.session_state.frames)} frames!")
                except Exception:
                    st.error("Invalid array - use comma separated integers")

        # Display array info
        try:
            _arr_preview = [int(x.strip()) for x in st.session_state.arr_text.split(",") if x.strip()!='']
            st.write(f"Array size: {len(_arr_preview)}")
        except Exception:
            st.write("Array size: 0")

    # (Playback and speed moved to bottom bar)

# Main display
image_placeholder = st.empty()

def get_algo_data():
    """Returns a dictionary of algorithm details."""
    return {
        "Bubble Sort": {
            "description": "A simple algorithm that repeatedly steps through the list, swapping adjacent elements if they are out of order.",
            "time_complexity": "O(n²) Average/Worst",
            "space_complexity": "O(1)"
        },
        "Selection Sort": {
            "description": "Repeatedly finds the minimum element from the unsorted part and places it at the beginning of the sorted part.",
            "time_complexity": "O(n²) Average/Worst",
            "space_complexity": "O(1)"
        },
        "Insertion Sort": {
            "description": "Builds the final sorted array one item at a time, much like sorting a hand of playing cards.",
            "time_complexity": "O(n²) Average/Worst",
            "space_complexity": "O(1)"
        },
        "Binary Search": {
            "description": "Searches a sorted array by repeatedly dividing the search interval in half.",
            "time_complexity": "O(log n) Average/Worst",
            "space_complexity": "O(1)"
        }
    }


# Bottom Bar: fixed-style container at the bottom (stays visible)
bottom = st.container()
with bottom:
    st.markdown(
        """
        <style>
        .fixed-bottom-bar {position: fixed; left: 0; right: 0; bottom: 12px; padding: 10px 16px; background: rgba(18,18,18,0.95); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; margin: 0 12px; z-index: 1000;}
        .fixed-bottom-spacer {height: 112px;}
        .playback-info {text-align: right;}
        .playback-info .step {font-weight: 800; font-size: 22px; letter-spacing: 0.2px; margin-bottom: 4px;}
        .playback-info .action {font-size: 18px; font-weight: 600; opacity: 0.95;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.frames:
        st.markdown('<div class="fixed-bottom-bar">', unsafe_allow_html=True)

        # Playback row
        c_left, c_mid, c_right = st.columns([3, 2, 5])
        with c_left:
            b1, b2, b3, b4 = st.columns([1,1,1,1])
            with b1:
                if st.button("≪", key="reset_btn", help="Reset"):
                    st.session_state.playing = False
                    st.session_state.idx = 0
            with b2:
                if st.button("‹", key="step_back_btn", help="Step Back"):
                    st.session_state.playing = False
                    st.session_state.idx = max(st.session_state.idx - 1, 0)
            with b3:
                # Single toggle button with clear text + icon
                play_label = "❚❚"
                pause_label = "▶"
                if st.button(pause_label if st.session_state.playing else play_label, key="play_pause_btn", help="Play/Pause"):
                    st.session_state.playing = not st.session_state.playing
            with b4:
                if st.button("›", key="step_forward_btn", help="Step Forward"):
                    st.session_state.playing = False
                    st.session_state.idx = min(st.session_state.idx + 1, max(len(st.session_state.frames) - 1, 0))

        with c_mid:
            # Replaced popover/radio with a slider for speed control
            st.session_state.speed_mult = st.slider(
                "Animation Speed",
                min_value=0.25,
                max_value=4.0,
                value=st.session_state.get('speed_mult', 1.0),
                step=0.25,
                format="%.2fx",
                key="speed_slider"
            )

        with c_right:
            step_placeholder = st.empty()
            info_placeholder = st.empty()
            if st.session_state.frames and 0 <= st.session_state.idx < len(st.session_state.frames):
                frame = st.session_state.frames[st.session_state.idx]
                step_placeholder.markdown(f"<div class='playback-info'><div class='step'>Step: {st.session_state.idx} / {len(st.session_state.frames)-1}</div></div>", unsafe_allow_html=True)
                _info_txt = str(frame.get('info', '')).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                info_placeholder.markdown(f"<div class='playback-info'><div class='action'>{_info_txt}</div></div>", unsafe_allow_html=True)
            else:
                step_placeholder.markdown("<div class='playback-info'><div class='step'>Step: 0 / 0</div></div>", unsafe_allow_html=True)
                info_placeholder.markdown("<div class='playback-info'><div class='action'></div></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        # Spacer to ensure content not hidden behind fixed bar
        st.markdown('<div class="fixed-bottom-spacer"></div>', unsafe_allow_html=True)
    else:
        # Intro content when no frames yet
        st.subheader("Welcome to Algorithm Visualizer")
        st.write("Configure an algorithm and data in the left sidebar, then click Visualize to see an animated step-by-step walkthrough.")
        
    st.markdown("---")
    st.header("About the Algorithms")

    ALGO_DATA = get_algo_data()

    for algo_name, data in ALGO_DATA.items():
        st.subheader(algo_name)
        st.write(data["description"])
        st.markdown(f"""
        - **Time Complexity:** `{data['time_complexity']}`
        - **Space Complexity:** `{data['space_complexity']}`
        """)
        st.markdown("---")
def render_frame_at(i: int):
    if 0 <= i < len(st.session_state.frames):
        frame = st.session_state.frames[i]
        fig = draw_state_fig(frame.get('state', []), frame.get('highlight', ()), frame.get('info', ''))
        image_placeholder.pyplot(fig)
        plt.close(fig)
        # Update right info area live
        try:
            step_placeholder.markdown(f"**Step:** {i} / {len(st.session_state.frames)-1}")
            info_placeholder.write(frame.get('info', ''))
        except Exception:
            pass

# Always render current frame if present
if st.session_state.frames:
    render_frame_at(st.session_state.idx)

# Smooth blocking playback that updates only placeholders (image + info)
if st.session_state.playing and st.session_state.frames:
    base_delay_ms = 1000
    delay = max(0.001, (base_delay_ms / max(0.1, st.session_state.speed_mult)) / 1000.0)
    for i in range(st.session_state.idx + 1, len(st.session_state.frames)):
        if not st.session_state.playing:
            break
        st.session_state.idx = i
        render_frame_at(i)
        time.sleep(delay)
    st.session_state.playing = False

