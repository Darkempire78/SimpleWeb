from rich.console import Console
from rich.panel import Panel

from utils import clear

class History():
    def __init__(self):
        self.console = Console()
        self.history = []
    
    def add(self, title, link):
        self.history.insert(
            0,
            {
                "title": title,
                "link": link
            }
        )
    
    def get(self):
        return self.history

    def displayHistory(self):
        clear()

        self.console.rule("[bold yellow]HISTORY")

        n = 0
        for tab in self.history:
            n += 1
            data = ""
            # Tab number
            data += f"[bold blue][{n}][/bold blue] "
            # Tab title
            data += f"[bold]{tab['title']}[/bold]"
            # Tab link
            data += f"\n[i red]{tab['link']}[/i red]"

            self.console.print(Panel(data))
