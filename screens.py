from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Center
from rich.text import Text

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
        colors = ["#EE3232", "#9393C2", "#D77878"]
        
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != ' ':
                    color_index = (x + y) % len(colors)
                    style = f"bold {colors[color_index]} on black"
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
