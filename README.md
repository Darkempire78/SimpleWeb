# SimpleWeb

![](https://img.shields.io/codefactor/grade/github/Darkempire78/SimpleWeb?style=for-the-badge) ![](https://img.shields.io/github/repo-size/Darkempire78/SimpleWeb?style=for-the-badge) ![](https://img.shields.io/badge/SOURCERY-ENABLED-green?style=for-the-badge) <a href="https://discord.com/invite/sPvJmY7mcV"><img src="https://img.shields.io/discord/831524351311609907?color=%237289DA&label=DISCORD&style=for-the-badge"></a>

Browse the internet easily from the console.

## Installation

* Install all dependencies : ``pip install -r requirements.txt``.
* Edit `config.example.json`:

```Javascript
{
    "resultPreviewLimit": 5, // 0 = Fast, 5 = Recommended, 10+= Slow
    "resultLimit": 20,
    "defaultBrowser": "google", // available: google, duckduckgo and brave
    "browserPrefixes": {
        "-g": "google",
        "-d": "duckduckgo",
        "-b": "brave"
    },
    "browserSearch": {
        "google": "https://www.google.com/search?q=",
        "duckduckgo": "https://html.duckduckgo.com/html?q=",
        "brave": "https://search.brave.com/search?q="
    },
    "browserDomainsBackList":{
        "google": [
            "https://www.google.", 
            "https://google.", 
            "https://webcache.googleusercontent.", 
            "http://webcache.googleusercontent.", 
            "https://policies.google.",
            "https://support.google.",
            "https://maps.google."
        ],
        "duckduckgo": [
            "https://duckduckgo.com/feedback.html",
            "https://help.duckduckgo.com/duckduckgo-help-pages/company/ads-by-microsoft-on-duckduckgo-private-search",
            "https://duckduckgo.com/y.js?ad_provider=",
            "https://html.duckduckgo.com/html/"
        ],
        "brave": [
            "https://search.brave.com",
            "https://brave.com/terms-of-use/",
            "https://brave.com/download/",
            "https://brave.com/transparency/",
            "https://status.brave.com/"
        ]
    },
    "spaceBetweenResults": true,
    "clear": true,
    "removeYoutubeResults": true,
    "removeGoogleTranslatorResults": true,
    "blackListDomains": [],
    "blackListTags": ["script", "head", "footer", "header", "style", "button", "iframe", "img", "picture", "video", "svg", "span", "form", "nav", "menu", "input"] // You can remove "span" if it takes away important information
}
```
* Rename it to `config.json`.

Finally, launch the script.

## Features

* History system
* Tab system
* Google, DuckDuckGo and BraveSearch support
* Customizable
* And more...

## Commands

| Commands                    | Action                                                                         |
|-----------------------------|--------------------------------------------------------------------------------|
| **:s** \<query>  <br> **:search** \<query> | Search the query on the default browser (write the number of the result to see the website) |
| **:s** -\<browserPrefix> \<query>  <br> **:search** -\<browserPrefix> \<query> | Search the query on a specific browser (write the number of the result to see the website) |
| **:ws** \<url> <br> **:website** \<url>    | Display a website                                                              |
| **:h** <br> **:history**                 | See the history                                                                |
| **:t** <br> **:tab** <br> **:tabs**               | See the list of tabs                                                           |
| **:t** -s \<tabNumber>           | Select a specific tab                                                          |
| **:t** \<query>                  | Create a new tab and search the query on Google                                |
| **:c** <br> **:clear**                   | Clear                                                                          |
| **:config**                     | Display the settings                                                           |

## Preview

### Search
<img src="assets/capture1.png" width="700"/>

### Website
<img src="assets/capture3.png" width="700"/>

### History
<img src="assets/capture2.png" width="700"/>

## Discord

Join the Discord server !

[![](https://i.imgur.com/UfyvtOL.png)](https://discord.gg/sPvJmY7mcV)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is under [GPLv3](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/LICENSE).
