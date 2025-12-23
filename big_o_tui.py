from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Input, Label, SelectionList, Log, TabbedContent, TabPane
from textual.worker import Worker
from textual_plotext import PlotextPlot

import time
import sys
import os

# Import logic from our existing sandbox
# Ensure big_o_sandbox is in the path or same directory
try:
    import big_o_sandbox
except ImportError:
    # If running from a different dir, try appending CWD
    sys.path.append(os.getcwd())
    import big_o_sandbox

class BigOTUI(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    #sidebar {
        dock: left;
        width: 30%;
        height: 100%;
        border-right: solid $primary;
        padding: 1 2;
        background: $surface;
    }

    #main-content {
        width: 70%;
        height: 100%;
        padding: 1;
    }

    .box {
        height: auto;
        border: solid $secondary;
        padding: 1;
        margin-bottom: 1;
    }

    Label {
        margin-bottom: 1;
        color: $text-disabled;
    }

    Button {
        width: 100%;
        margin-top: 2;
    }
    
    SelectionList {
        height: 15;
        border: solid $accent;
    }
    
    Input {
        margin-bottom: 1;
    }
    """

    TITLE = "Big O Visualizer (TUI)"
    SUB_TITLE = "Powered by Textual & Plotext"

    def compose(self) -> ComposeResult:
        # Sidebar for controls
        with Container(id="sidebar"):
            yield Label("Configuration")
            
            yield Label("Select Algorithms:")
            # Generate selection list from imported ALGORITHMS
            # ALGORITHMS is dict: "1": ("O(1)", func)
            # Use tuples for SelectionList: (label, value, initial_state)
            selections = []
            for key, (name, _) in big_o_sandbox.ALGORITHMS.items():
                # Default select O(n) and O(n^2)
                initial_state = (key in ["3", "5"])
                selections.append((name, key, initial_state))
            
            yield SelectionList(*selections, id="algo-list")

            yield Label("Range (Start, End, Step):")
            with Vertical(classes="box"):
                yield Input(placeholder="Start", value="100", id="start-n", type="integer")
                yield Input(placeholder="End", value="1000", id="end-n", type="integer")
                yield Input(placeholder="Step", value="100", id="step-n", type="integer")

            yield Button("Run Comparison", variant="primary", id="run-btn")
            yield Button("Quit", variant="error", id="quit-btn")

        # Main content area with Tabs
        with Container(id="main-content"):
            with TabbedContent(initial="plot-tab"):
                with TabPane("Visualization", id="plot-tab"):
                    yield PlotextPlot(id="plot-widget")
                
                with TabPane("Execution Log", id="log-tab"):
                    yield Log(id="log-widget")
                
                with TabPane("Definitions", id="def-tab"):
                    # Quick help text
                    text = "\n".join([f"{k}: {v}" for k, v in big_o_sandbox.EXPLANATIONS.items()])
                    yield Static(text)

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if btn_id == "quit-btn":
            self.exit()
        elif btn_id == "run-btn":
            self.run_comparison()

    def run_comparison(self):
        log = self.query_one("#log-widget", Log)
        plot_widget = self.query_one("#plot-widget", PlotextPlot)
        
        # Get Inputs
        try:
            start_n = int(self.query_one("#start-n").value)
            end_n = int(self.query_one("#end-n").value)
            step_n = int(self.query_one("#step-n").value)
            
            if start_n < 1 or end_n <= start_n or step_n < 1:
                log.write_line("[!] Invalid range input.")
                self.notify("Invalid Range!", severity="error")
                return
        except ValueError:
            log.write_line("[!] Inputs must be integers.")
            self.notify("Inputs must be integers!", severity="error")
            return

        # Get Selected Algorithms
        selection_list = self.query_one("#algo-list", SelectionList)
        selected_keys = selection_list.selected
        
        if not selected_keys:
            log.write_line("[!] No algorithms selected.")
            self.notify("Select at least one algorithm!", severity="warning")
            return
            
        # Prepare Data
        # Map keys back to (name, function)
        selected_algs = [big_o_sandbox.ALGORITHMS[k] for k in selected_keys]
        
        log.write_line(f"Running test: N=[{start_n}..{end_n}], Step={step_n}")
        log.write_line(f"Algorithms: {[a[0] for a in selected_algs]}")
        
        # Run in worker to avoid freezing UI
        self.run_worker(self.compute_and_plot(selected_algs, range(start_n, end_n + 1, step_n)), exclusive=True)

    async def compute_and_plot(self, algorithms, n_range):
        plot_widget = self.query_one("#plot-widget", PlotextPlot)
        log = self.query_one("#log-widget", Log)
        
        # We need to gather data to plot lines: X axis = N, Y axis = Time
        # data_store = { "O(1)": [t1, t2...], "O(n)": [t1, t2...] }
        x_axis = list(n_range)
        data_store = {alg[0]: [] for alg in algorithms}
        
        plot_widget.plt.clear_data()
        plot_widget.plt.title("Runtime Complexity")
        plot_widget.plt.xlabel("Input Size (N)")
        plot_widget.plt.ylabel("Time (seconds)")
        
        # Computation loop
        for n in n_range:
            for name, func in algorithms:
                t = big_o_sandbox.measure_time(func, n)
                if t is None: t = 0
                data_store[name].append(t)
            
            # Optional: Intermediate log
            # log.write_line(f"Finished N={n}...")
            # We could do partial updates here if plotext supports it easily, 
            # but usually it's cleaner to plot at end or in chunks.
            
        # Plotting
        for name, times in data_store.items():
            plot_widget.plt.plot(x_axis, times, label=name)
        
        plot_widget.refresh()
        log.write_line("Test Complete. Graph updated.")
        self.notify("Comparison Complete")

if __name__ == "__main__":
    app = BigOTUI()
    app.run()
