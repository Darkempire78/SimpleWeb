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
from markdownify import markdownify as md


class SimpleWeb:
    def __init__(self):
        self.query = None
        self.console = Console()

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

    def scrapeGoogle(self, query, urlDataLimit=8):

        tree = Tree(f"[bold blue]{query}[/bold blue]")

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
            tree.add(f"[b][{n}][/b] [i red]{link}[/i red]" + ('\n[bold]'+ title + '[/bold]' if title else '') + ('\n' + description if description else '') + "\n")
            
        self.clear()
        print(tree)

        website = int(input("Select a website: "))
        link = links[website - 1]
        websiteMD = self.htmlToMarkdown(link)
        print(websiteMD)
        self.clear()
        self.console.print(Panel(websiteMD))


    def htmlToMarkdown(self, url):
        r = requests.get(url)
        markdown = md(r.text)
        markdown = Markdown(markdown)
        return markdown

if __name__ == '__main__':
    SW = SimpleWeb()
    SW.scrapeGoogle(input("Search: "))