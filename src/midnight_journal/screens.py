from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Center
from rich.text import Text

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

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
            gradient_colors.extend(interpolate_colors(base_colors[i], base_colors[i+1], 20))

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