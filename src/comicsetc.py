import requests
from bs4 import BeautifulSoup

def comic_etc_search(search_string):
    """Search https://www.comicsetc.com.au/
    81 Elizabeth St, Brisbane City QLD 4000"""
    shop = "Comic Etc"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.comicsetc.com.au/search?q="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN COMIC ETC THEY USE VOLUME INSTEAD OF VOL

    search_list = [x.lower() for x in search_list]
    if "vol" in search_list:
        search_list = [ "volume" if x=="vol" else x for x in search_list]
    
    full_search_url = base_search_url + separator.join(search_list)
    #print(full_search_url)

    #GET WEB PAGE
    response = requests.get(full_search_url)

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')

        # MAIN SECTION OF RESULTS
        main_section = soup.main

        # GET ALL OBJECTS WITH CLASS=ARTICLE
        list_of_articles = main_section.find_all("article")
        
        for article in list_of_articles:
            comic_title = article.h4.text.strip()

            comic_url = "https://www.comicsetc.com.au"+article.find_all("a")[2]["href"].strip()

            comic_price = article.span.text.strip()
            comic_price = float(comic_price.replace("$", ""))

            comic = {"title": comic_title,
                     "url": comic_url,
                     "price": comic_price,
                     "shop":shop,
                     "availability": "In Stock (auto)"}
            # DO SOME MATCHING
            # CRUDE = TAKE ALL 3+ LETTER WORDS IN SEARCH AND SEE IF THEY ARE IN COMIC TITLE
            list_word_search = [x.lower() for x in search_list if len(x)> 2]

            list_word_title = comic_title.split(" ")
            list_word_title = [x.lower() for x in list_word_title if len(x)> 2]
            # REMOVE COLONS
            list_word_title = [x.replace(":","") for x in list_word_title]

            #print(list_word_search)
            #print(list_word_title)
            # IF ALL WORDS FROM SEARCH ARE IN TITLE: RETURN
            if all(item in list_word_title for item in list_word_search):
                result_holder.append(comic)

            
        
    # ON FAILURE    
    else:
        print('An error has occurred searching Comics Etc.')

    return result_holder