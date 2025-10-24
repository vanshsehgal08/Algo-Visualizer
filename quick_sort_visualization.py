import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def quicksort(arr, start=0, end=None):
    """
    Generator function that implements Quick Sort and yields the state at each step.
    
    Yields:
        tuple: (array, pivot_idx, left, right, start, end, message)
    """
    if end is None:
        end = len(arr) - 1
        
    if start >= end:
        return

    # Choose random pivot and move it to the start
    pivot_idx = random.randint(start, end)
    arr[start], arr[pivot_idx] = arr[pivot_idx], arr[start]
    pivot_idx = start
    pivot_val = arr[pivot_idx]
    
    left = start + 1
    right = end
    
    # Initial state before partitioning
    yield arr.copy(), pivot_idx, left, right, start, end, "Starting new partition"
    
    while left <= right:
        # Find element on left that should be on right
        while left <= right and arr[left] <= pivot_val:
            yield arr.copy(), pivot_idx, left, right, start, end, "Moving left pointer"
            left += 1
            
        # Find element on right that should be on left
        while left <= right and arr[right] >= pivot_val:
            yield arr.copy(), pivot_idx, left, right, start, end, "Moving right pointer"
            right -= 1
            
        if left <= right:
            # Swap elements and continue
            arr[left], arr[right] = arr[right], arr[left]
            yield arr.copy(), pivot_idx, left, right, start, end, f"Swapped {arr[right]} and {arr[left]}"
            left += 1
            right -= 1
    
    # Move pivot to its final position
    arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
    pivot_idx = right
    yield arr.copy(), pivot_idx, left, right, start, end, "Pivot in final position"
    
    # Recursively sort subarrays
    yield from quicksort(arr, start, pivot_idx - 1)
    yield from quicksort(arr, pivot_idx + 1, end)

def update_plot(frame_data, bars, text, colors):
    """
    Update function for the animation.
    """
    arr, pivot_idx, left, right, start, end, message = frame_data
    
    # Update bar heights
    for i, bar in enumerate(bars):
        bar.set_height(arr[i])
        
        # Set colors based on current state
        if i == pivot_idx:
            bar.set_color('yellow')  # Pivot
        elif i == left or i == right:
            bar.set_color('red')     # Pointers
        elif start <= i <= end:
            bar.set_color('#1f77b4') # Active sub-array
        else:
            bar.set_color('lightgrey') # Inactive
    
    # Update text
    text.set_text(message)
    
    return bars

def visualize_quicksort(arr, save_path=None):
    """
    Visualize the Quick Sort algorithm.
    
    Args:
        arr (list): List of numbers to sort
        save_path (str, optional): If provided, saves the animation to this path
    """
    # Create figure and axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), 
                                  gridspec_kw={'height_ratios': [4, 1]})
    
    # Set up the main plot
    ax1.set_title('Quick Sort Visualization')
    ax1.set_xlim(0, len(arr))
    ax1.set_ylim(0, max(arr) * 1.1)
    
    # Create bars and text
    bars = ax1.bar(range(len(arr)), arr, color='#1f77b4')
    text = ax2.text(0.5, 0.5, '', ha='center', va='center', fontsize=12)
    ax2.axis('off')
    
    # Create animation
    frames = quicksort(arr.copy())
    anim = FuncAnimation(fig, update_plot, frames=frames, 
                        fargs=(bars, text, None), 
                        interval=800, repeat=False, 
                        cache_frame_data=False)
    
    # Save or show the animation
    if save_path:
        anim.save(save_path, writer='pillow', fps=2)
    else:
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Example usage
    random.seed(42)  # For reproducible results
    n = 15
    arr = [random.randint(1, 100) for _ in range(n)]
    print("Original array:", arr)
    
    # Visualize the sorting process
    visualize_quicksort(arr)
    
    # To save the animation:
    # visualize_quicksort(arr, save_path='quicksort_animation.gif')
