import urllib
import os
import requests
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


class SimpleWeb:
    def __init__(self):
        self.console = Console()
        self.query = None
        self.current = {
            "type": None,
            "data": None
        }
        self.back = {
            "type": None,
            "data": None
        }

    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

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

    def scrapeGoogle(self, back=False, query=None, urlDataLimit=8):

        if back:
            newBack = self.current.copy()
            self.current = self.back.copy()
            self.back = newBack
            query = self.query
            links = [i["link"] for i in self.current["data"]]
        else:
            self.back = self.current.copy()
            self.current["type"] = "searchResult"
            self.query = query
            self.current["data"] = []

        tree = Tree(f"[bold blue]{query}[/bold blue]")

        if back is False:
            query = urllib.parse.quote_plus(query)
            response = self.getSource("https://www.google.com/search?q=" + query)

            links = list(response.html.absolute_links)
            google_domains = ('https://www.google.', 
                            'https://google.', 
                            'https://webcache.googleusercontent.', 
                            'http://webcache.googleusercontent.', 
                            'https://policies.google.',
                            'https://support.google.',
                            'https://maps.google.')

            for url in links[:]:
                if url.startswith(google_domains):
                    links.remove(url)

        n = 0
        for link in track(links, description="[blue]Searching:[/blue]", total=len(links)):
            n += 1
            if back:
                title = self.current["data"][n - 1]["title"]
                description = self.current["data"][n - 1]["description"]
            else:
                if n <= urlDataLimit:
                    self.clear()
                    print(tree)
                title = None 
                description = None 
                if n <= urlDataLimit:
                    r = requests.get(link)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    try:
                        # title = soup.select("meta[name='twitter:title']")[0].attrs["content"]
                        title = soup.select("meta[property='og:title']")[0].attrs["content"]
                    except:
                        pass
                    try:
                        # description = soup.select("meta[name='twitter:description']")[0].attrs["content"]
                        description = soup.select("meta[property='og:description']")[0].attrs["content"]
                    except:
                        pass
            self.current["data"].append(
                {
                    "link": link,
                    "title": title,
                    "description": description
                }
            )
            tree.add(f"[b][{n}][/b] [i red]{link}[/i red]" + ('\n[bold]'+ title + '[/bold]' if title else '') + ('\n' + description if description else '') + "\n")
            
        self.clear()
        print(tree)

        self.inputHandler()


    def htmlToMarkdown(self, url):
        r = requests.get(url)
        markdown = md(r.text)
        markdown = Markdown(markdown)
        return markdown

    def displayWebPage(self, back=False, link=None):

        if back:
            websiteMD = self.back["data"]
        else:
            websiteMD = self.htmlToMarkdown(link)
        
        self.clear()

        self.back = self.current.copy()

        self.console.print(Panel(websiteMD))

        self.current["type"] = "webPage"
        self.current["data"] = websiteMD

        self.inputHandler()

    def inputHandler(self):
        try:
            choice = Prompt.ask("[bold blue]Action[/bold blue]")
            prefix = choice.split(" ")[0]
            if prefix == ":s":
                self.scrapeGoogle(query=choice[2:])
            elif prefix == ":b" and self.back["type"] != None:
                if self.back["type"] == "webPage":
                    self.displayWebPage(back=True)
                elif self.back["type"] == "searchResult":
                    self.scrapeGoogle(back=True)
            else:
                if self.current["type"] == "searchResult":
                    link = self.current["data"][int(choice) - 1]["link"]
                    self.displayWebPage(link=link)
                else:
                    self.console.print("[i red]Invalid query[/i red]")
                    self.inputHandler()
        except Exception as ex:
            print(ex)
            self.inputHandler()


if __name__ == '__main__':
    SW = SimpleWeb()
    SW.scrapeGoogle(query=Prompt.ask("Search"))