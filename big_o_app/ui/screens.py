from textual.screen import Screen
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Button, Static

class IntroScreen(Screen):
    CSS = """
    IntroScreen {
        align: center middle;
        background: $surface;
    }
    #intro-container {
        width: 60;
        height: auto;
        border: thick $primary;
        padding: 2;
        background: $surface-lighten-1;
        text-align: center;
    }
    #title {
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
        text-align: center;
    }
    #desc {
        margin-bottom: 2;
        color: $text;
    }
    Button {
        width: 100%;
    }
    """

    def compose(self):
        yield Header()
        with Container(id="intro-container"):
            yield Static("Welcome to Big O Visualizer", id="title")
            yield Static(
                "Explore Algorithm Complexity Interactively!\n\n"
                "• Compare standard algorithms.\n"
                "• Visualize runtime growth.\n"
                "• Teaching Mode: Learn safely.\n"
                "• Chaos Mode: Test limits (at your own risk!).\n\n"
                "Press the button below to start your experiment.",
                id="desc"
            )
            yield Button("Start Experimenting", variant="primary", id="start-btn")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-btn":
            self.app.pop_screen()
