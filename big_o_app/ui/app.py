from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Label, SelectionList, Button, Input, Log, TabbedContent, TabPane, Static, RadioButton, RadioSet, Switch, Header
from textual_plotext import PlotextPlot
from rich.table import Table
import asyncio

from ..config import EXPLANATIONS, AppState
from ..algorithms import ALGORITHMS
from ..engine.timer import measure_time
from .viz import plot_external
from .screens import IntroScreen

class BigOTUI(App):
    """
    Main Application class for the Big O Visualizer.
    Manages state, UI composition, and algorithm execution workers.
    """
    CSS = """
    Screen { layout: horizontal; }
    #sidebar { dock: left; width: 30%; height: 100%; border-right: solid $primary; padding: 1 2; background: $surface; }
    #main-content { width: 70%; height: 100%; padding: 1; }
    .box { height: auto; border: solid $secondary; padding: 1; margin-bottom: 1; }
    Label { margin-bottom: 1; color: $text-disabled; }
    Button { width: 100%; margin-top: 1; }
    SelectionList { height: 10; border: solid $accent; }
    Input { margin-bottom: 1; }
    RadioSet { border: solid $secondary; padding: 1; height: auto; margin-bottom: 1; }
    
    .error { border: solid $error; }
    .teaching-mode { background: $success-darken-3; color: $text; }
    .chaos-mode { background: $error-darken-3; color: $text; }
    """

    TITLE = "Big O Visualizer"
    SUB_TITLE = "Teaching Mode"
    
    last_results = {}
    last_algorithms = []
    last_range = None
    worker = None # Track current worker

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.push_screen(IntroScreen())

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, id="header")
        
        with Container(id="sidebar"):
            yield Label("Mode:")
            with RadioSet(id="mode-selector"):
                yield RadioButton("Teaching Mode", value=True, id="mode-teaching")
                yield RadioButton("Chaos Mode", id="mode-chaos")
            
            yield Label("Configuration")
            
            selections = []
            for key, (name, _) in ALGORITHMS.items():
                initial_state = (key in ["3", "5"])
                selections.append((name, key, initial_state))
            
            yield Label("Select Algorithms:")
            yield SelectionList(*selections, id="algo-list")

            yield Label("Range (Start, End, Step):")
            yield Input(placeholder="Start", value="100", id="start-n", type="integer", tooltip="Starting input size.")
            yield Input(placeholder="End", value="1000", id="end-n", type="integer", tooltip="Ending input size.")
            yield Input(placeholder="Step", value="100", id="step-n", type="integer", tooltip="Step increment.")
            
            yield Label("Options:")
            with RadioSet(id="plot-type"):
                yield RadioButton("Line Plot", value=True, id="mode-line")
                yield RadioButton("Scatter Plot", id="mode-scatter")
            
            # Simplified Safety Display (controlled by Mode)
            yield Label("Safety: ON (Teaching)", id="safety-label")

            yield Button("Run Comparison", variant="primary", id="run-btn", tooltip="Start the visualization.")
            yield Button("Abort Test", variant="warning", id="abort-btn", disabled=True, tooltip="Emergency stop.")
            yield Button("Open in Matplotlib", id="ext-btn", tooltip="View high-res chart in external window.")
            yield Button("Quit", variant="error", id="quit-btn")

        with Container(id="main-content"):
            with TabbedContent(initial="plot-tab"):
                with TabPane("Visualization", id="plot-tab"):
                    yield PlotextPlot(id="plot-widget")
                
                with TabPane("Execution Log", id="log-tab"):
                    yield Log(id="log-widget")
                
                with TabPane("Help & Definitions", id="def-tab"):
                    # Augmented Help Text
                    help_text = (
                        "HOW TO USE:\n"
                        "1. Select a Mode (Teaching vs Chaos).\n"
                        "2. Choose Algorithms to compare.\n"
                        "3. Set N Range (e.g., 100 to 1000).\n"
                        "4. Click Run.\n\n"
                        "DEFINITIONS:\n" + 
                        "\n".join([f"{k}: {v}" for k, v in EXPLANATIONS.items()])
                    )
                    yield Static(help_text)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit-btn":
            self.exit()
        elif event.button.id == "run-btn":
            self.run_comparison()
        elif event.button.id == "ext-btn":
            self.open_external_plot()
        elif event.button.id == "abort-btn":
            if self.worker:
                self.worker.cancel()
                self.query_one("#log-widget", Log).write_line("[!] Aborting...")

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        if event.radio_set.id == "mode-selector":
            safety_label = self.query_one("#safety-label", Label)
            header = self.query_one("#header", Header)
            
            if self.query_one("#mode-teaching", RadioButton).value:
                # Teaching Mode
                AppState.mode = "TEACHING"
                AppState.safety_enabled = True
                AppState.delay = 0.05
                self.sub_title = "Teaching Mode (Safety ON, Slow)"
                safety_label.update("Safety: ON")
                header.classes = "teaching-mode"
                header.remove_class("chaos-mode")
            else:
                # Chaos Mode
                AppState.mode = "CHAOS"
                AppState.safety_enabled = False
                AppState.delay = 0.0
                self.sub_title = "CHAOS MODE (Safety OFF, Fast)"
                safety_label.update("Safety: OFF (DANGER)")
                header.classes = "chaos-mode"
                header.remove_class("teaching-mode")
                
                self.notify("WARNING: Chaos Mode enabled. Limits removed.", severity="warning", timeout=5)

    def validate_inputs(self):
        try:
            start_inp = self.query_one("#start-n", Input)
            end_inp = self.query_one("#end-n", Input)
            step_inp = self.query_one("#step-n", Input)
            
            start_n = int(start_inp.value)
            end_n = int(end_inp.value)
            step_n = int(step_inp.value)
            
            valid = True
            if start_n < 1: 
                start_inp.add_class("error")
                valid = False
            else: start_inp.remove_class("error")
                
            if end_n <= start_n:
                end_inp.add_class("error")
                valid = False
            else: end_inp.remove_class("error")
                
            if step_n < 1:
                step_inp.add_class("error")
                valid = False
            else: step_inp.remove_class("error")
                
            if not valid: return None
            return (start_n, end_n, step_n)
            
        except ValueError:
            return None

    def run_comparison(self):
        log = self.query_one("#log-widget", Log)
        
        vals = self.validate_inputs()
        if not vals:
            self.notify("Invalid Input Range!", severity="error")
            return
            
        start_n, end_n, step_n = vals
        selected_keys = self.query_one("#algo-list", SelectionList).selected
        if not selected_keys:
            self.notify("Select at least one algorithm!", severity="warning")
            return
            
        selected_algs = [ALGORITHMS[k] for k in selected_keys]
        plot_type = "line" if self.query_one("#mode-line", RadioButton).value else "scatter"
        
        log.write_line(f"Starting: Mode={AppState.mode}")
        
        self.last_range = range(start_n, end_n + 1, step_n)
        self.last_algorithms = selected_algs
        
        # UI State update
        self.query_one("#run-btn").disabled = True
        self.query_one("#abort-btn").disabled = False
        
        self.worker = self.run_worker(self.compute_and_plot(selected_algs, self.last_range, plot_type), exclusive=True)

    async def compute_and_plot(self, algorithms, n_range, plot_type):
        plot_widget = self.query_one("#plot-widget", PlotextPlot)
        log = self.query_one("#log-widget", Log)
        
        plot_widget.plt.clear_data()
        plot_widget.plt.title(f"Complexity ({plot_type.title()})")
        
        x_axis = []
        # Structure for live updates: {alg_name: [times...]}
        # We need to build lists incrementally
        results = {name: [] for name, _ in algorithms}
        
        try:
            for n in n_range:
                # Check cancellation
                # In Textual workers, cancellation raises CancelledError at await points, 
                # but we are doing CPU blocking work in measure_time. 
                # We should yield control regularly.
                
                x_axis.append(n)
                
                for name, func in algorithms:
                    t = measure_time(func, n)
                    results[name].append(t)
                
                # --- LIVE UPDATE OR DELAY ---
                if AppState.delay > 0:
                    # Teaching mode: Simulate "thinking" or emphasis
                    await asyncio.sleep(AppState.delay)
                    log.write_line(f"Processed N={n}...")
                    
                # Yield to UI loop (allows Abort button click to be processed)
                await asyncio.sleep(0.01)

            # Final Plot
            for name, times in results.items():
                clean_times = [t if t is not None else 0 for t in times]
                if plot_type == "line":
                    plot_widget.plt.plot(x_axis, clean_times, label=name)
                else:
                    plot_widget.plt.scatter(x_axis, clean_times, label=name)
            
            self.last_results = results
            self.last_results = results
            plot_widget.refresh()
            
            # --- SUMMARY TABLE ---
            self.print_summary_table(log, results, len(x_axis))
            
            log.write_line("Test Complete.")
            self.notify("Test Complete", severity="information")
            
        except asyncio.CancelledError:
            log.write_line("[!] Test Aborted by User.")
            self.notify("Test Aborted")
            
        finally:
            self.query_one("#run-btn").disabled = False
            self.query_one("#abort-btn").disabled = True
            self.worker = None

    def print_summary_table(self, log_widget, results, count):
        """Generates and prints a summary table to the log."""
        if count == 0: return

        table = Table(title="Performance Summary")
        table.add_column("Algorithm", style="cyan")
        table.add_column("Max Time (s)", justify="right")
        table.add_column("Avg Time (s)", justify="right")
        
        for name, times in results.items():
             # Filter Nones
             valid_times = [t for t in times if t is not None]
             if not valid_times:
                 table.add_row(name, "N/A", "N/A")
                 continue
                 
             max_t = max(valid_times)
             avg_t = sum(valid_times) / len(valid_times)
             
             table.add_row(name, f"{max_t:.6f}", f"{avg_t:.6f}")
        
        log_widget.write(table)
