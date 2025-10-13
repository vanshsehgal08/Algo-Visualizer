import time
import random
import streamlit as st
import matplotlib.pyplot as plt

# --- Mock algorithm functions for stand-alone execution ---
# (In your actual project, you would import these from your files)
def bubble_sort(arr):
    n = len(arr)
    yield {"state": arr.copy(), "highlight": (), "info": "Initial array"}
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            yield {"state": arr.copy(), "highlight": (j, j + 1), "info": f"Comparing {arr[j]} and {arr[j+1]}"}
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield {"state": arr.copy(), "highlight": (j, j + 1), "info": f"Swapping {arr[j+1]} and {arr[j]}"}
        if not swapped:
            break
    yield {"state": arr.copy(), "highlight": (), "info": "Array is sorted"}

def insertion_sort(arr):
    yield {"state": arr.copy(), "highlight": (), "info": "Initial array"}
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        yield {"state": arr.copy(), "highlight": (i, j), "info": f"Select {key} to insert"}
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            yield {"state": arr.copy(), "highlight": (j, j + 1), "info": f"Shifting {arr[j]} right"}
            j -= 1
        arr[j + 1] = key
        yield {"state": arr.copy(), "highlight": (j + 1,), "info": f"Inserted {key}"}
    yield {"state": arr.copy(), "highlight": (), "info": "Array is sorted"}

def selection_sort(arr):
    n = len(arr)
    yield {"state": arr.copy(), "highlight": (), "info": "Initial array"}
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield {"state": arr.copy(), "highlight": (min_idx, j), "info": f"Finding minimum in unsorted part"}
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield {"state": arr.copy(), "highlight": (i, min_idx), "info": f"Swapping minimum {arr[i]} to position {i}"}
    yield {"state": arr.copy(), "highlight": (), "info": "Array is sorted"}

def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    yield {"state": arr, "highlight": (low, high), "info": f"Initial search range: index {low} to {high}"}
    while low <= high:
        mid = (low + high) // 2
        yield {"state": arr, "highlight": (low, mid, high), "info": f"Checking middle index {mid} (value: {arr[mid]})"}
        if arr[mid] == target:
            yield {"state": arr, "highlight": (mid,), "info": f"Target {target} found at index {mid}"}
            return
        elif arr[mid] < target:
            low = mid + 1
            yield {"state": arr, "highlight": (low, high), "info": f"Target is greater. New range: {low} to {high}"}
        else:
            high = mid - 1
            yield {"state": arr, "highlight": (low, high), "info": f"Target is smaller. New range: {low} to {high}"}
    yield {"state": arr, "highlight": (), "info": f"Target {target} not found in the array"}
# --- End of mock functions ---


ALGOS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
}

def draw_state_fig(state, highlight=(), info=""):
    """Draws a bar chart with axis labels, title, and highlight indices."""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 3))
    if not isinstance(state, (list, tuple)) or (len(state) and isinstance(state[0], (list, tuple))):
        ax.text(0.5, 0.5, str(state), ha='center', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
    else:
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
        for rect, val in zip(bars, state):
            height = rect.get_height()
            ax.annotate(f'{val}', xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)
    plt.tight_layout()
    return fig

st.set_page_config(page_title="Algorithm Visualizer", layout="wide")
if 'algo_name' not in st.session_state:
    st.session_state.algo_name = "Bubble Sort"
st.title(f"Algorithm Visualizer — {st.session_state.algo_name}")

# --- UI STATE DEFAULTS ---
if 'setup_visible' not in st.session_state:
    st.session_state.setup_visible = True
if 'manual_arr_text' not in st.session_state:
    st.session_state.manual_arr_text = "5,2,4,1,3"
if 'rand_size' not in st.session_state:
    st.session_state.rand_size = 10
if 'rand_seed' not in st.session_state:
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
if 'input_method' not in st.session_state:
    st.session_state.input_method = "Manual Input"


# --- SIDEBAR CONTROLS ---
with st.sidebar:
    with st.expander("Setup Panel", expanded=st.session_state.setup_visible):
        
        algo_name = st.selectbox("Algorithm", list(ALGOS.keys()) + ["Binary Search"])
        st.session_state.algo_name = algo_name

        st.markdown("**Data Input**")
        
        # --- FIX: Moved radio button outside the form ---
        # This allows it to trigger a rerun and update the UI immediately.
        st.radio(
            "Data Source",
            ("Manual Input", "Generate Random"),
            key='input_method'
        )

        with st.form("visualization_form"):
            # --- FIX: Conditional UI is now inside the form ---
            # It will display the correct input based on the radio button's state
            if st.session_state.input_method == "Manual Input":
                st.text_area(
                    "Enter comma-separated values",
                    key="manual_arr_text",
                    height=80,
                )
            else: # "Generate Random" is selected
                size = st.slider("Array Size", min_value=2, max_value=50, value=st.session_state.rand_size, key="rand_size_slider")
                # Automatically update the random array preview if size changes
                if size != st.session_state.rand_size or not st.session_state.rand_array:
                    rng = random.Random(st.session_state.rand_seed)
                    st.session_state.rand_array = [rng.randint(1, 99) for _ in range(size)]
                    st.session_state.rand_size = size
                
                preview = ",".join(map(str, st.session_state.rand_array))
                st.code(preview)


            if algo_name == "Binary Search":
                target = st.number_input("Target value", value=5, key="target_value")

            visualize_submit = st.form_submit_button("Visualize", use_container_width=True, type="primary")

            if visualize_submit:
                try:
                    if st.session_state.input_method == "Manual Input":
                        source_text = st.session_state.manual_arr_text
                    else: # Generate Random
                        source_text = ",".join(map(str, st.session_state.rand_array))
                    
                    arr = [int(x.strip()) for x in source_text.split(",") if x.strip() != '']
                    
                    if not arr:
                        st.error("Please enter at least one number")
                    else:
                        if algo_name == "Binary Search":
                            st.session_state.frames = list(binary_search(sorted(arr), int(st.session_state.target_value)))
                        else:
                            st.session_state.frames = list(ALGOS[algo_name](arr))
                        st.session_state.idx = 0
                        st.session_state.playing = False
                        st.success(f"Generated {len(st.session_state.frames)} frames!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    try:
        if st.session_state.get('input_method') == "Manual Input":
            current_text = st.session_state.get('manual_arr_text', "")
        else:
            current_text = ",".join(map(str, st.session_state.get('rand_array', [])))
        _arr_preview = [int(x.strip()) for x in current_text.split(",") if x.strip() != '']
        st.write(f"Array size: {len(_arr_preview)}")
    except Exception:
        st.write("Array size: 0")


# --- MAIN DISPLAY & PLAYBACK ---
image_placeholder = st.empty()

def get_algo_data():
    """Returns a dictionary of algorithm details."""
    return {
        "Bubble Sort": {"description": "A simple algorithm that repeatedly steps through the list, swapping adjacent elements if they are out of order.", "time_complexity": "O(n²) Average/Worst", "space_complexity": "O(1)"},
        "Selection Sort": {"description": "Repeatedly finds the minimum element from the unsorted part and places it at the beginning of the sorted part.", "time_complexity": "O(n²) Average/Worst", "space_complexity": "O(1)"},
        "Insertion Sort": {"description": "Builds the final sorted array one item at a time, much like sorting a hand of playing cards.", "time_complexity": "O(n²) Average/Worst", "space_complexity": "O(1)"},
        "Binary Search": {"description": "Searches a sorted array by repeatedly dividing the search interval in half.", "time_complexity": "O(log n) Average/Worst", "space_complexity": "O(1)"}
    }

# --- BOTTOM BAR ---
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
        c_left, c_mid, c_right = st.columns([3, 2, 5])
        with c_left:
            b1, b2, b3, b4 = st.columns([1,1,1,1])
            if b1.button("≪", key="reset_btn", help="Reset"):
                st.session_state.playing = False
                st.session_state.idx = 0
                st.rerun()
            if b2.button("‹", key="step_back_btn", help="Step Back"):
                st.session_state.playing = False
                st.session_state.idx = max(st.session_state.idx - 1, 0)
                st.rerun()
            play_label = "▶" if not st.session_state.playing else "❚❚"
            if b3.button(play_label, key="play_pause_btn", help="Play/Pause"):
                st.session_state.playing = not st.session_state.playing
                st.rerun()
            if b4.button("›", key="step_forward_btn", help="Step Forward"):
                st.session_state.playing = False
                st.session_state.idx = min(st.session_state.idx + 1, max(len(st.session_state.frames) - 1, 0))
                st.rerun()

        with c_mid:
            st.session_state.speed_mult = st.slider("Animation Speed", min_value=0.25, max_value=4.0, value=st.session_state.get('speed_mult', 1.0), step=0.25, format="%.2fx", key="speed_slider")

        with c_right:
            step_placeholder = st.empty()
            info_placeholder = st.empty()
            if st.session_state.frames and 0 <= st.session_state.idx < len(st.session_state.frames):
                frame = st.session_state.frames[st.session_state.idx]
                step_placeholder.markdown(f"<div class='playback-info'><div class='step'>Step: {st.session_state.idx} / {len(st.session_state.frames)-1}</div></div>", unsafe_allow_html=True)
                _info_txt = str(frame.get('info', '')).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
                info_placeholder.markdown(f"<div class='playback-info'><div class='action'>{_info_txt}</div></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="fixed-bottom-spacer"></div>', unsafe_allow_html=True)
    else:
        st.subheader("Welcome to Algorithm Visualizer")
        st.write("Configure an algorithm and data in the left sidebar, then click Visualize to see an animated step-by-step walkthrough.")
        st.markdown("---")
        st.header("About the Algorithms")
        ALGO_DATA = get_algo_data()
        for algo_name, data in ALGO_DATA.items():
            st.subheader(algo_name)
            st.write(data["description"])
            st.markdown(f"""- **Time Complexity:** `{data['time_complexity']}`\n- **Space Complexity:** `{data['space_complexity']}`""")
            st.markdown("---")

def render_frame_at(i: int):
    if 0 <= i < len(st.session_state.frames):
        frame = st.session_state.frames[i]
        fig = draw_state_fig(frame.get('state', []), frame.get('highlight', ()), frame.get('info', ''))
        image_placeholder.pyplot(fig)
        plt.close(fig)

# Playback loop
def run_playback():
    if st.session_state.playing and st.session_state.frames:
        base_delay_ms = 1000
        delay = max(0.001, (base_delay_ms / max(0.1, st.session_state.speed_mult)) / 1000.0)
        
        while st.session_state.idx < len(st.session_state.frames) - 1:
            if not st.session_state.playing:
                break
            st.session_state.idx += 1
            render_frame_at(st.session_state.idx)
            # A short sleep is necessary for the UI to feel responsive
            time.sleep(delay)
        
        st.session_state.playing = False
        st.rerun()

# --- SCRIPT EXECUTION FLOW ---
if st.session_state.frames:
    render_frame_at(st.session_state.idx)
if st.session_state.playing:
    run_playback()