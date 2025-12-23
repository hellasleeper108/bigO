# Big O Visualizer

A powerful, interactive Terminal User Interface (TUI) for exploring algorithm time complexity. Built with **Python**, **Textual**, and **Plotext**.

![Big O Visualizer TUI](https://raw.githubusercontent.com/placeholder/repo/main/docs/screenshot.png)

## Features

*   **Interactive TUI**: A modern terminal interface with mouse support, tabs, and live graphs.
*   **Dual Modes**:
    *   **Teaching Mode**: Safety rails enforced, slower updates for learning, green theme.
    *   **Chaos Mode**: Limits removed, raw execution speed, red theme.
*   **Real-time Visualization**:
    *   **TUI**: Live Line or Scatter plots directly in your terminal.
    *   **External**: Export data to a high-resolution **Matplotlib** window for detailed analysis.
*   **Algorithm Library**: Compare O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n), and O(n!).
*   **Safety Rails**: Prevents freezing your machine by aborting dangerous operations (e.g., O(n!) with N=20).

## Installation

Requires Python 3.8+.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/big-o-visualizer.git
    cd big-o-visualizer
    ```

2.  **Install dependencies**:
    ```bash
    pip install textual plotext matplotlib
    ```

## Usage

Run the modular application package:

```bash
python -m big_o_app.main
```

### Controls

*   **Sidebar**:
    *   **Mode**: Switch between Teaching and Chaos modes.
    *   **Algorithms**: Select which functions to benchmarks.
    *   **Range**: Set Start, End, and Step for input size N.
    *   **Chart Type**: Toggle Line vs Scatter.
    *   **Actions**: Run Comparison, Open in Matplotlib, or Quit.
*   **Abort**: Cancel any running test immediately.

## Project Structure

This project has been refactored into a scalable modular architecture:

```text
big_o_app/
├── main.py                # Entry point
├── config.py              # Configuration & State
├── algorithms/            # Algorithm implementations
├── engine/                # Measurement & Safety logic
└── ui/                    # Textual UI components
    ├── app.py             # Main App logic
    ├── screens.py         # Intro screens
    └── viz.py             # Matplotlib integration
```

## Contributing

Contributions are welcome! Please open an issue or submit a PR for new algorithms or visualization features.

## License

MIT
