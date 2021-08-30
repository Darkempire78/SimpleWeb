from utils import clear
from rich.console import Console
from rich.panel import Panel

class Tabs:
    def __init__(self):
        self.console = Console()
        self.tabs = []
        self.currentTab = 0

    def display(self):
        clear()

        self.console.rule("[bold yellow]TABS")

        n = 0
        for tab in self.tabs:
            n += 1
            data = ""
            # Tab number
            data += f"[bold blue][{n}][/bold blue] "
            if n - 1 == self.currentTab:
                data += "[bold blue](CURRENT)[/bold blue] "
            # Tab title
            if tab["current"]["type"] == "webPage":
                data += f"[bold]{tab['current']['data']['results']['title']}[/bold]"
            elif tab["current"]["type"] == "searchResult":
                data += f"[bold]Search: {tab['current']['data']['query']}[/bold]"
            else:
                data += f"[bold]Empty Page[/bold]"
            # Tab link
            if tab["current"]["type"] == "webPage":
                data += f"\n[i red]{tab['current']['data']['results']['link']}[/i red]"
            elif tab["current"]["type"] == "searchResult":
                pass
            else:
                pass
            self.console.print(Panel(data))

    def new(self, query=None):
        clear()
        # Create a new tab
        self.tabs.append(
            {
                "history": [],
                "current": {
                    "type": None,
                    "data": {}
                }
            }
        )
        self.currentTab = len(self.tabs) -1

    def changeCurrent(self, tab=None):
        clear()

        if not tab.isdigit():
            self.console.print("[i red]Invalid tab, it must be a number[/i red]")
        elif int(tab) <= 0 or int(tab)>= len(self.tabs):
            self.console.print(f"[i red]Invalid tab, the number selected is higher than {len(self.tabs) -1} or less than 1[/i red]")
        else:
            self.currentTab = int(tab) - 1

        self.inputHandler()