# Big O Sandbox

A single-file Python interactive educational tool for exploring time complexities.

![Big O Growth](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Comparison_computational_complexity.svg/600px-Comparison_computational_complexity.svg.png)
*(Image concept: Visualizing growth)*

## Features

- **Interactive Menu**: Easy navigation between modes.
- **Automated Complexity Test**: Run a full suite O(1) through O(n^2) with ASCII visualizations.
- **Comparison Mode**: Fight two algorithms side-by-side to see who wins (and why).
- **Step-Through Mode**: Pause execution after each input size to "feel" the growth.
- **Curses Visualization**: (Optional) Dynamic bar charts using terminal graphics (`--curses`).
- **Safety Rails**: Limits specific to O(2ⁿ) and O(n!) to prevent infinite hanging.
- **Final Logic**: A summary screen that ranks algorithms and judges their practicality.

## Usage

### 1. Interactive Mode (Recommended)
Just run the script to enter the main menu:
```bash
python big_o_sandbox.py
```

### 2. Quick Command Line Args
- See explanations: `python big_o_sandbox.py --explain`
- Launch directly into Curses mode: `python big_o_sandbox.py --curses`

## Requirements
- Python 3.6+
- Standard libraries only (unless on Windows, where `curses` is optional but recommended).

## License
MIT
