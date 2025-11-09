from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.message import Message
from textual.widgets import Label, TextArea

from screens import WelcomeScreen


class JournalInput(TextArea):
    class Submitted(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()

    def _on_key(self, event: events.Key) -> None:
        self.app.log(f"Key event: {event!r}")
        if event.key == "shift+enter":
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
    }

    .wrapped_label {
      text-overflow: ellipsis;
      width: 100%;
      height: auto;
    }
    """

    def on_mount(self) -> None:
        self.screen.styles.background = "maroon"
        self.push_screen(WelcomeScreen())

    def compose(self) -> ComposeResult:
        yield Container(id="output-container")
        yield JournalInput(placeholder="Your thoughts here...", id="journal_input")

    def on_journal_input_submitted(self, event: JournalInput.Submitted) -> None:
          journal_input = event.value
          self.log(f"User entered: {journal_input}")
          output_container = self.query_one("#output-container")

          # Create new label from input text
          new_label = Label(journal_input, classes="wrapped_label")

          # Mount Label to the end of container
          output_container.mount(new_label)

          # Clear the input field
          self.query_one("#journal_input", JournalInput).text = ""


if __name__ == "__main__":
    app = MidnightJournal()
    app.run()