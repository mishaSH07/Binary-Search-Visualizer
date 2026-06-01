import os
import base64
import gradio as gr

# ---------- Paths / assets ----------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_image_data_uri(rel_path):
    """Read an image file and return a data: URI for use in <img src="...">."""
    full_path = os.path.join(BASE_DIR, rel_path)
    with open(full_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:image/png;base64,{b64}"


SHIP_IMG     = load_image_data_uri("images/ship.png")
ISLAND_IMG   = load_image_data_uri("images/island.png")
TREASURE_IMG = load_image_data_uri("images/treasure.png")


# ---------- Core binary search logic (step-based) ----------

def parse_array(array_str):
    """Parse a comma/space-separated string into a sorted list of ints."""
    if not array_str.strip():
        raise ValueError("Array cannot be empty.")
    parts = [p for chunk in array_str.split(",") for p in chunk.split()]
    nums = [int(p) for p in parts]
    nums.sort()
    return nums


def render_visual(state):
    """
    Build an HTML visualization showing the array as a row of islands with:
    - lo / hi boundary labels
    - ship icon at mid
    - treasure icon at found index
    - greyed-out islands outside the current search window
    """
    if state is None or "array" not in state:
        return "<p>Click <b>Start / Reset</b> to begin.</p>"

    arr         = state["array"]
    lo          = state["lo"]
    hi          = state["hi"]
    mid         = state.get("mid")
    target      = state["target"]
    found_index = state.get("found_index")
    step        = state["step"]
    finished    = state["finished"]

    base_style = (
        "display:inline-block;margin:6px;padding:8px 10px;"
        "text-align:center;font-family:monospace;"
    )

    islands_html = []
    for i, val in enumerate(arr):
        island_opacity = 1.0 if lo <= i <= hi else 0.35

        # lo / hi labels
        lh_labels = []
        if i == lo:
            lh_labels.append("L")
        if i == hi:
            lh_labels.append("H")
        label_row = (
            "<div style='font-size:14px;margin-bottom:4px;'>"
            + " ".join(lh_labels)
            + "</div>"
        ) if lh_labels else ""

        # Icons overlaid on top of the island image
        overlay_icons = ""
        if i == mid:
            overlay_icons += (
                f"<img src='{SHIP_IMG}' alt='ship' style='"
                "position:absolute;top:50%;left:50%;"
                "transform:translate(-50%,-65%);"
                "width:44px;height:44px;object-fit:contain;pointer-events:none;'/>"
            )
        if i == found_index:
            overlay_icons += (
                f"<img src='{TREASURE_IMG}' alt='found' style='"
                "position:absolute;top:50%;left:50%;"
                "transform:translate(-50%,-35%);"
                "width:40px;height:40px;object-fit:contain;pointer-events:none;'/>"
            )

        island_wrapper = (
            "<div style='position:relative;display:inline-block;width:80px;height:80px;'>"
            f"<img src='{ISLAND_IMG}' alt='island' "
            f"style='width:80px;height:80px;object-fit:contain;opacity:{island_opacity};display:block;'/>"
            f"{overlay_icons}"
            "</div>"
        )
        index_label = f"<div style='margin-top:4px;font-size:14px;'>[{i}] = {val}</div>"

        islands_html.append(
            f"<div style='{base_style}'>{label_row}{island_wrapper}{index_label}</div>"
        )

    header = f"<h3>Step {step}</h3>"
    summary = f"<p>Target: <b>{target}</b> | lo = {lo}, hi = {hi}, mid = {mid}</p>"

    if finished:
        if found_index is not None:
            status = (
                "<p style='color:green;font-size:32px;font-weight:bold;margin-top:20px;'>"
                f"Found at index {found_index} (value = {arr[found_index]}).</p>"
            )
        else:
            status = (
                "<p style='color:red;font-size:32px;font-weight:bold;margin-top:20px;'>"
                "Target not found in array.</p>"
            )
    else:
        status = "<p>Click <b>Next step</b> to continue.</p>"

    return header + summary + "".join(islands_html) + status


def start_search(array_str, target):
    """Initialize state for a new binary search run."""
    try:
        arr = parse_array(array_str)
    except ValueError as e:
        return (
            f"<p style='color:red;'>Input error: {e}</p>",
            "Please fix the input and press Start again.",
            None,
        )

    if len(arr) == 0:
        return (
            "<p style='color:red;'>Array cannot be empty.</p>",
            "Please provide at least one number.",
            None,
        )

    state = {
        "array":       arr,
        "target":      int(target),
        "lo":          0,
        "hi":          len(arr) - 1,
        "mid":         None,
        "step":        0,
        "finished":    False,
        "found_index": None,
    }

    visual = render_visual(state)
    explanation = (
        "Array parsed and sorted.\n\n"
        f"- Values: {arr}\n"
        f"- Target: {target}\n"
        "- At each step the midpoint is checked and half the remaining range is discarded."
    )
    return visual, explanation, state


def next_step(state):
    """Perform one step of binary search and return updated visual, explanation, and state."""
    if state is None or "array" not in state:
        return (
            "<p style='color:red;'>No active search. Click <b>Start / Reset</b> first.</p>",
            "No state — please initialize the search first.",
            state,
        )

    if state["finished"]:
        return (
            render_visual(state),
            "Search already finished. Press Start / Reset to try a new example.",
            state,
        )

    arr    = state["array"]
    target = state["target"]
    lo     = state["lo"]
    hi     = state["hi"]
    step   = state["step"] + 1

    if lo > hi:
        state.update(finished=True, step=step, mid=None)
        return (
            render_visual(state),
            "Search window collapsed (lo > hi). Target is not in the array.",
            state,
        )

    mid = (lo + hi) // 2
    val = arr[mid]
    state["mid"]  = mid
    state["step"] = step

    if val == target:
        state.update(finished=True, found_index=mid)
        explain = (
            f"Step {step}:\n"
            f"- Checked index {mid} → value {val}.\n"
            "- Value matches the target. Search complete."
        )
    elif val < target:
        old_lo     = lo
        state["lo"] = mid + 1
        explain = (
            f"Step {step}:\n"
            f"- Checked index {mid} → value {val}.\n"
            f"- {val} < {target}: target is in the RIGHT half.\n"
            f"- Discarded indices {old_lo}–{mid}. New window: lo = {state['lo']}, hi = {hi}."
        )
    else:
        old_hi      = hi
        state["hi"] = mid - 1
        explain = (
            f"Step {step}:\n"
            f"- Checked index {mid} → value {val}.\n"
            f"- {val} > {target}: target is in the LEFT half.\n"
            f"- Discarded indices {mid}–{old_hi}. New window: lo = {lo}, hi = {state['hi']}."
        )

    return render_visual(state), explain, state


# ---------- Helper: generate arrays from range + parity ----------

def generate_array_from_range(start, end, mode):
    """
    Return a comma-separated string of ints in [start, end] filtered by parity.
    mode: 'Even' | 'Odd' | 'Both'
    """
    try:
        start, end = int(start), int(end)
    except (TypeError, ValueError):
        return "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

    if end <= start:
        return str(start)

    if mode == "Even":
        first = start if start % 2 == 0 else start + 1
        nums = list(range(first, end + 1, 2))
    elif mode == "Odd":
        first = start if start % 2 != 0 else start + 1
        nums = list(range(first, end + 1, 2))
    else:
        nums = list(range(start, end + 1))

    return ", ".join(str(x) for x in nums)


# ---------- Gradio UI ----------

with gr.Blocks(title="Binary Search Visualizer") as demo:
    gr.Markdown(
        """
# Binary Search Visualizer

Generate a sorted array (or type your own), set a target value, click **Start / Reset**,
then step through the binary search one iteration at a time with **Next step**.
"""
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Array Generator (optional)")
            range_start = gr.Number(label="Start value (inclusive)", value=1,  precision=0)
            range_end   = gr.Number(label="End value (inclusive, > start)", value=10, precision=0)
            parity_mode = gr.Radio(
                label="Include which numbers?",
                choices=["Both", "Even", "Odd"],
                value="Both",
            )
            generate_button = gr.Button("Generate array from range")

        with gr.Column():
            gr.Markdown("### Array and Target")
            array_input = gr.Textbox(
                label="Array (numbers)",
                value="1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
                placeholder="Example: 1, 2, 3, 4, 5",
            )
            target_input = gr.Number(label="Target value", value=7, precision=0)

    start_button = gr.Button("Start / Reset")
    step_button  = gr.Button("Next step")

    visual_output      = gr.HTML(label="Array View")
    explanation_output = gr.Markdown(label="Step Explanation")

    search_state = gr.State()

    generate_button.click(
        fn=generate_array_from_range,
        inputs=[range_start, range_end, parity_mode],
        outputs=array_input,
    )

    start_button.click(
        fn=start_search,
        inputs=[array_input, target_input],
        outputs=[visual_output, explanation_output, search_state],
    )

    step_button.click(
        fn=next_step,
        inputs=[search_state],
        outputs=[visual_output, explanation_output, search_state],
    )

if __name__ == "__main__":
    demo.launch()
