# Oz Comics Search
## Support your (geographically distant) local comic book store (online).

### Download GUI app
- To come (will bundle the gui script with pyinstaller or py2app)

### Why
Because I live in a part of Australia with no local comic book store and found myself ordering online a lot, trying as much as possible to stick to Australian stores and limit ordering from big chains (Amazon AU, Bookdepository UK).
However both price and inventory varies a lot bwteen store so I ended up loosing time checking availability / comparing price.

### How (does it works)
Oz Comics Search is very simple. 
It takes a simple search term (the name of a series) and optionally a book type (Trade / Issue) and a book number.
It then interrogate what would be the first web-page of results on each store and scrape the Title / Price / URL.

### Which Store is included 
Oz Comics Search checks the following stores (in alphabetical order):
- [AllStar Comics](https://allstarcomics.com.au/) - Melbourne
- Amazon AU (only books shipped by Amazon AU from AU)
- [Area 52](https://area52.circlesoft.net/) - Hobart
- BookDepository and Booktopia
- [ComicsEtc](https://www.comicsetc.com.au/) - Brisbane
- [Comics'R'Us](https://comicsrus.com.au/) - Melbourne/Windsor
- [Greenlight Comics](https://greenlightcomics.com/) - Adelaide
- [Impact Comics](https://impactcomics.com.au/) - Canberra
- [Incognito Comics](https://www.incognitocomics.com.au/) - Melbourne
- [Mac's Comics](https://www.macscomics.com.au/) - Mackay
- [Minotaur](https://www.minotaur.com.au/) - Melbourne
- [PopCultcha](https://www.popcultcha.com.au) - Geelong
- [Secret HQ Comics](https://secrethqcomics.com.au/)- Melbourne - Beaconsfield

(Don't hesitate to suggest more in the issues)

I'm more of a trade person so I only kept stores with :
- An online store
- A descent offering of trade 
- An easy to scrape website

### Tutorial
- GUI VERSION: click search and then double click on an entry to open the page in browser
- CLI version:
  - First ```pip install bs4 requests```
  - Then for example:  
    - ```python oz_comic_search.py "search term in quotes" -b issue/trade -n number``` General Synthax (-b and -n are optional)
    - ```python oz_comic_search.py "batman flash button" -b issue```  for all single issues of BATMAN/THE FLASH the button
    -  ```python oz_comic_search.py "paper girls" -b trade` -n 6``` for the 6th Trade of Paper Girls 

### Caveat
Since this script works through web page scrapping, it **WILL** break if any changes are made to the store's online store (All store searches are functional as of 04/08/2021).
Code is also messy, I need to replace individual function for each store to a store class with a search method in the future.

(MIT LICENCE)
