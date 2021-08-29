import urllib
import requests
import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from rich import print
from rich.tree import Tree
from rich.progress import track
from rich.markdown import Markdown
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from markdownify import markdownify as md

from utils import clear


class SimpleWeb:
    def __init__(self):
        self.console = Console()

        with open("config.json", "r", encoding="utf-8") as configFile:
            config = json.load(configFile)

        self.resultPreviewLimit= config["resultPreviewLimit"]
        self.resultLimit= config["resultLimit"]
        self.spaceBetweenResults= config["spaceBetweenResults"]
        self.removeYoutubeResults= config["removeYoutubeResults"]
        self.removeGoogleTranslatorResults= config["removeGoogleTranslatorResults"]
        self.blackListDomains = config["blackListDomains"]
        self.blackListTags = config["blackListTags"]

        self.tabs = []
        self.currentTab = 0
        self.back = {
            "type": None,
            "data": {}
        }

    def getSource(self, url):
        """Return the source code for the provided URL. 

        Args: 
            url (string): URL of the page to scrape.

        Returns:
            response (object): HTTP response object from requests_html. 
        """
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    def scrapeGoogle(self, back=False, query=None):
        # if back:
        #     newBack = self.current.copy()
        #     self.current = self.back.copy()
        #     self.back = newBack
        #     query = self.current["data"]["query"]
        #     links = [i["link"] for i in self.current["data"]["results"]]
        # else:
            # self.back = self.current.copy()
        self.tabs[self.currentTab]["current"]["type"] = "searchResult"
        self.tabs[self.currentTab]["current"]["data"]["query"] = query
        self.tabs[self.currentTab]["current"]["data"]["results"] = []

        tree = Tree(f"[bold blue]{query}[/bold blue]")

        if back is False:
            query = urllib.parse.quote_plus(query)
            response = self.getSource("https://www.google.com/search?q=" + query)

            links = list(response.html.absolute_links)
            googleDomains = ('https://www.google.', 
                            'https://google.', 
                            'https://webcache.googleusercontent.', 
                            'http://webcache.googleusercontent.', 
                            'https://policies.google.',
                            'https://support.google.',
                            'https://maps.google.')
            
            youtubeDomains = ("https://www.youtube.com/")

            googleTransltaorDomains = ("https://translate.google.com/")

            for url in links[:]:
                if url.startswith(googleDomains):
                    links.remove(url)
                if self.removeYoutubeResults:
                    if url.startswith(youtubeDomains):
                        links.remove(url)
                if self.removeGoogleTranslatorResults:
                    if url.startswith(googleTransltaorDomains):
                        links.remove(url)
                if self.blackListDomains:
                    if url.startswith(self.blackListDomains):
                        links.remove(url)

        n = 0
        for link in track(links, description="[blue]Searching:[/blue]", total=len(links)):
            n += 1
            if n - 1 >= self.resultLimit:
                break
            # if back:
            #     title = self.tabs[self.currentTab]["current"]["data"]["results"][n - 1]["title"]
            #     description = self.tabs[self.currentTab]["current"]["data"]["results"][n - 1]["description"]
            # else:
            if n <= self.resultPreviewLimit:
                clear()
                print(tree)
            title = None 
            description = None 
            if n <= self.resultPreviewLimit:
                try:
                    r = requests.get(link)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    # title = soup.select("meta[name='twitter:title']")[0].attrs["content"]
                    title = soup.select("meta[property='og:title']")
                    if len(title) > 0:
                        title = title[0].attrs["content"]
                    else:
                        title = None
                    # description = soup.select("meta[name='twitter:description']")[0].attrs["content"]
                    description = soup.select("meta[property='og:description']")
                    if len(description) > 0:
                        description = description[0].attrs["content"]
                    else:
                        description = None
                except:
                    pass
            self.tabs[self.currentTab]["current"]["data"]["results"].append(
                {
                    "link": link,
                    "title": title,
                    "description": description
                }
            )
            tree.add(f"[b][{n}][/b] [i red]{link}[/i red]" + ('\n[bold]'+ title + '[/bold]' if title else '') + ('\n' + description if description else '') + ('\n' if self.spaceBetweenResults is True else ''))
            
        clear()
        print(tree)

        self.inputHandler()


    def htmlToMarkdown(self, url):
        r = requests.get(url)
        html = r.text
        # Remove script tags
        soup = BeautifulSoup(html, features="lxml")
        title = soup.find("title").text
        for s in soup.find_all(self.blackListTags):
            s.extract()
        markdown = md(str(soup))
        # markdown = md(html)
        markdown = Markdown(markdown)
        return (title, markdown)

    def displayWebPage(self, back=False, link=None):
        # if back:
        #     websiteMD = self.back["data"]["websiteMD"]
        #     link = self.back["data"]["link"]
        #     title = self.back["data"]["title"]
        # else:
        title, websiteMD = self.htmlToMarkdown(link)
        
        clear()

        # self.back = self.current.copy()

        self.console.print(Panel(f"[bold blue]{title}[/bold blue]\n[i yellow]{link}[/i yellow]"), Panel(websiteMD))

        self.tabs[self.currentTab]["current"]["type"] = "webPage"
        self.tabs[self.currentTab]["current"]["data"]["results"] = {
            "websiteMD": websiteMD,
            "title": title,
            "link": link
        }

        self.inputHandler()

    def displaySettings(self):
        clear()

        with open("config.json", "r", encoding="utf-8") as configFile:
            config = json.load(configFile)

        data = ""
        for key, value in config.items():
            data += f"[bold blue]{key}[/bold blue]: [red]{value}[/red]\n"
            
        self.console.print(Panel(data))

        self.inputHandler()

    def displayTabs(self):
        clear()

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

        self.inputHandler()

    def newTab(self, query=None):
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

        # Search the query
        self.scrapeGoogle(query=query)

        self.inputHandler()

    def changeCurrentTab(self, tab=None):
        clear()

        if not tab.isdigit():
            self.console.print("[i red]Invalid tab, it must be a number[/i red]")
        elif int(tab) <= 0 or int(tab)>= len(self.tabs):
            self.console.print(f"[i red]Invalid tab, the number selected is higher than {len(self.tabs) -1} or less than 1[/i red]")
        else:
            self.currentTab = int(tab) - 1

        self.inputHandler()

    def inputHandler(self):
        try:
            query = Prompt.ask("[bold blue]Search[/bold blue]").strip()
            prefix = query.split(" ")[0]
            if prefix == ":s"  or prefix == ":search":
                if len(query.split(" ")) <= 1:
                    self.console.print("[i red]Empty query[/i red]")
                    self.inputHandler()
                self.scrapeGoogle(query=query.replace(prefix, "", 1))
            if prefix == ":ws" or prefix == ":website":
                if len(query.split(" ")) <= 1:
                    self.console.print("[i red]Empty query[/i red]")
                    self.inputHandler()
                self.displayWebPage(link=query.replace(prefix, "", 1))
            # Clear
            elif prefix == ":c" or prefix == ":clear":
                clear()
                self.inputHandler()
            # Settings
            elif prefix == ":config":
                self.displaySettings()
            # Tabs
            elif prefix == ":t" or prefix == ":tab" or prefix == ":tabs":
                if query == prefix:
                    self.displayTabs()
                elif query.split(" ")[1] == "-s" or query.split(" ")[1] == "-select":
                    self.changeCurrentTab(query.split(" ")[2])
                else:
                    self.newTab(query=query.replace(prefix, "", 1))
            # Back
            # elif prefix == ":b":
            #     if self.back["type"] is None:
            #         self.console.print("[i red]There is nothing back[/i red]")
            #         self.inputHandler()
            #     if self.back["type"] == "webPage":
            #         self.displayWebPage(back=True)
            #     elif self.back["type"] == "searchResult":
            #         self.scrapeGoogle(back=True)
            else:
                if self.tabs[self.currentTab]["current"]["type"] == "searchResult" and query.isdigit():
                    link = self.tabs[self.currentTab]["current"]["data"]["results"][int(query) - 1]["link"]
                    self.displayWebPage(link=link)
                else:
                    self.console.print("[i red]Invalid query[/i red]")
                    self.inputHandler()
        except Exception as ex:
            print(ex)
            self.inputHandler()

    def main(self):
        # Check if a tab is opened
        if not self.tabs:
            self.currentTab = 0
            self.tabs.append(
                {
                    "history": [],
                    "current": {
                        "type": None,
                        "data": {}
                    }
                }
            )
        
        self.inputHandler()


if __name__ == '__main__':
    SW = SimpleWeb()
    SW.main()