---
title: Binary Search Visualizer
emoji: 🔍
colorFrom: blue
colorTo: yellow
sdk: gradio
sdk_version: "6.0.2"
app_file: app.py
pinned: false
license: mit
---

# Binary Search Visualizer

An interactive Gradio app that visualizes the binary search algorithm step by step. Each element of the array is shown as an island; a ship icon marks the current midpoint, and a treasure chest marks the found value.

## Name

**Misha Shubin**

## Algorithm Name

**Binary Search**

## Demo screenshots

First view loaded in:
![loadingin](https://raw.githubusercontent.com/mishaSH07/Binary-Search-Visualizer/main/images/initialss.png)

Mid binary search:
![midsearch](https://raw.githubusercontent.com/mishaSH07/Binary-Search-Visualizer/main/images/midsearchss.png)

Target found:
![targetfound](https://raw.githubusercontent.com/mishaSH07/Binary-Search-Visualizer/main/images/treasurefoundss.png)

Target not found:
![targetnotfound](https://raw.githubusercontent.com/mishaSH07/Binary-Search-Visualizer/main/images/treasurenotfoundss.png)

## Problem Breakdown & Computational Thinking

### Decomposition: What smaller steps form your chosen algorithm?

- Parse Input
    - Read array as a comma/space-separated string
    - Convert to `List[int]` and sort ascending
    - Read target value as `int`

- Initialize Search State
    - `lo = 0`, `hi = len(array) - 1`
    - `mid = None`, `step = 0`, `finished = False`, `found_index = None`
    - Store everything in a state dictionary that Gradio passes between calls

- Single Search Step
    - If `lo > hi`: mark not found and stop
    - Compute `mid = (lo + hi) // 2`
    - Compare `arr[mid]` with target:
        - Equal → mark found and stop
        - Less → move `lo = mid + 1`
        - Greater → move `hi = mid - 1`

- Visual Updates
    - Return updated HTML visualization and a text explanation for each step
    - Connect buttons to the core binary search functions

### Pattern Recognition: How does it repeatedly reach, compare, or swap values?

- Recognizes that the array is sorted
- Repeats the divide-and-conquer pattern:
    - Jump to the middle index between `lo` and `hi`
    - Compare `arr[mid]` to target
    - Discard the half that cannot contain the target
- The same pattern runs every step until:
    - A match is found, or
    - `lo > hi` (target does not exist in the array)

- Visual repetition:
    - The ship icon always moves to the current midpoint island
    - Islands outside the current window are faded out

### Abstraction: Which details are shown to the user and which are hidden?

- Shown to the user:
    - Island row (array elements)
    - L / H boundary pointers and the ship at mid
    - Step-by-step status and explanation text

- Hidden from the user:
    - Image data-URI encoding
    - Gradio UI internals

### Algorithm Design: Input → Processing → Output

![Binary Search Flowchart](https://raw.githubusercontent.com/mishaSH07/Binary-Search-Visualizer/main/images/finalprojectflowchart.png)

**Data types / structures**

- Array (islands)
    - GUI: text (Gradio `Textbox`, comma/space-separated integers)
    - Internal: `List[int]` after parsing and sorting

- Target value
    - GUI: numeric (Gradio `Number`)
    - Internal: `int`

- Search state (single dictionary)
  ```
  state = {
      "array":       List[int],
      "target":      int,
      "lo":          int,
      "hi":          int,
      "mid":         Optional[int],
      "step":        int,
      "finished":    bool,
      "found_index": Optional[int],
  }
  ```

- Generator inputs
    - `range_start: int`, `range_end: int`, `mode: str ("Both" | "Even" | "Odd")`
    - Output: comma-separated string that populates the array textbox

## Steps to Run

### Locally in VS Code

1. Clone the repo
2. Open the folder in VS Code
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Run the app: `python app.py`
6. Open the local Gradio URL shown in the terminal (typically http://127.0.0.1:7860/)

### On Hugging Face

Visit: https://huggingface.co/spaces/MishaShubin/Binary-Search-Visualizer

## Author & Acknowledgment

Author: Misha Shubin  
Course: CISC 121 Final Project  
Algorithm: Binary Search

AI Usage Disclosure:
- ChatGPT (GPT-4) was used to:
    - Help design the Gradio interface for step-by-step visualization
    - Assist with the state dictionary structure
    - All generated code was reviewed, tested, and integrated manually into the final project
