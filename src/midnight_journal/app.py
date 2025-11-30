import os
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Center, Vertical
from textual.message import Message
from textual.widgets import Label, TextArea, Markdown, Button, Static
from textual.screen import Screen
from rich.text import Text

DATA_DIR = "../../data"
JOURNAL_FILE = os.path.join(DATA_DIR, "journal.md")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)


def interpolate_colors(start_hex, end_hex, steps):
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    interpolated_colors = []
    for i in range(steps):
        interpolated_rgb = [
            int(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * i / (steps - 1))
            for j in range(3)
        ]
        interpolated_colors.append(rgb_to_hex(tuple(interpolated_rgb)))
    return interpolated_colors


class WelcomeScreen(Screen):
    def compose(self):
        art = """
███╗   ███╗██╗██████╗ ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗   
████╗ ████║██║██╔══██╗████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝
██╔████╔██║██║██║  ██║██╔██╗ ██║██║██║  ███╗███████║   ██║   
██║╚██╔╝██║██║██║  ██║██║╚██╗██║██║██║   ██║██╔══██║   ██║  
██║ ╚═╝ ██║██║██████╔╝██║ ╚████║██║╚██████╔╝██║  ██║   ██║
╚═╝     ╚═╝╚═╝╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝

            """

        rich_art = Text()
        lines = art.splitlines()
        base_colors = ["#EE3232", "#9393C2", "#D77878", "#EE3232"]

        gradient_colors = []
        # Interpolate between each pair of colors
        for i in range(len(base_colors) - 1):
            gradient_colors.extend(interpolate_colors(base_colors[i], base_colors[i + 1], 20))

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != ' ':
                    color_index = (x + y) % len(gradient_colors)
                    style = f"bold {gradient_colors[color_index]} on black"
                    rich_art.append(char, style=style)
                else:
                    rich_art.append(' ')
            rich_art.append('\n')

        yield Center(
            Static(rich_art),
            Button("Start Journaling", variant="primary", id="start_button")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_button":
            self.dismiss()

class JournalInput(TextArea):
    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def _on_key(self, event: events.Key) -> None:
        self.app.log(f"Key event: {event!r}")
        if event.key == "shift+enter":
            self.styles.height = self.styles.height.value + 1
            self.replace("\n", self.selection.start, self.selection.end)
            event.prevent_default()
            return

        if event.key == "enter":
            event.prevent_default()
            self.post_message(self.Submitted(self.text))
            return

        super()._on_key(event)

class MidnightJournal(App):
    """Midnight Journal App"""

    CSS = """
    #journal_input {
        dock: bottom;
        width: 100%;
        height: 3; /* Adjust height as needed */
        border: solid #5E1F1F;
    }

    #output-container{
      padding-left: 1;
      overflow-y: scroll;
      height: 1fr;
    }

    .wrapped_label {
      text-overflow: ellipsis;
      width: 100%;
      height: auto;
    }
    #start_button {
      background: #5E1F1F;
      border: solid #5E1F1F;
      width: auto;
    }
    Screen {
        align: center middle;
    }
    """

    def on_mount(self) -> None:
        self.screen.styles.background = "red 30%"
        self.push_screen(WelcomeScreen())
        
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Load existing journal entries
        if os.path.exists(JOURNAL_FILE):
            with open(JOURNAL_FILE, "r") as f:
                content = f.read()
                output_container = self.query_one("#output-container")
                entries = content.split("\n\n")
                for entry in entries:
                    if entry:
                        output_container.mount(Markdown(entry, classes="wrapped_label"))
                output_container.scroll_end(animate=False)


    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(id="output-container"),
            JournalInput(placeholder="Your thoughts here...", id="journal_input")
        )

    def on_journal_input_submitted(self, event: JournalInput.Submitted) -> None:
          journal_input = event.value
          self.log(f"User entered: {journal_input}")
          
          # Save to file
          with open(JOURNAL_FILE, "a") as f:
              f.write(journal_input + "\n\n")
              
          output_container = self.query_one("#output-container")

          # Create new Markdown widget from input text
          new_label = Markdown(journal_input, classes="wrapped_label")

          # Mount Label to the end of container
          output_container.mount(new_label)

          # Clear the input field
          self.query_one("#journal_input", JournalInput).text = ""
          # Reset the height of the input field
          self.query_one("#journal_input", JournalInput).styles.height = 3
          # Scroll to the end of the output container
          output_container.scroll_end(animate=True)


if __name__ == "__main__":
    app = MidnightJournal()
    app.run()
