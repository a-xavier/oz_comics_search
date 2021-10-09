import requests
from bs4 import BeautifulSoup
def comicsrus_search(search_string):
    """
    Search https://comicsrus.com.au/
    114 Chapel Street
    Windsor Victoria 3181

    Telephone: +61-3-9510 1584

    Email: shop@comicsrus.com.au
    """
    shop = "Comics 'R' Us"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://comicsrus.com.au/search?q="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN COMICS R US THEY USE VOL INSTEAD OF VOL

    search_list = [x.lower() for x in search_list]
    if "volume" in search_list:
        search_list = [ "vol" if x=="volume" else x for x in search_list]

    full_search_url = base_search_url + separator.join(search_list)

    #print(full_search_url)

    #GET WEB PAGE
    response = requests.get(full_search_url, headers={"User-Agent":"Defined"})

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')

        # GET ALL OBJECTS WITH CLASS=ARTICLE
          # last ITEM IS NOT A REAL SEARCH RESULT
        list_of_products = soup.find('div', class_ = "grid").find_all('div', class_ = "grid")

        for article in list_of_products:

            comic_title = article.h3.text

            comic_url = "https://comicsrus.com.au" + article.a["href"]

            # SPLITTING FOR WHEN IT HAS REDUCED PRICE TOO

            comic_price = article.span.text

            comic_price = float(comic_price.replace("$",""))

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
            # REMOVE COLONS, coma
            list_word_title = [x.replace(":","") for x in list_word_title]
            list_word_title = [x.replace(";","") for x in list_word_title]
            list_word_title = [x.replace(",","") for x in list_word_title]
            list_word_title = [x.replace(".","") for x in list_word_title]
            list_word_title = [x.replace("(","") for x in list_word_title]
            list_word_title = [x.replace(")","") for x in list_word_title]

            #print(list_word_search)
            #print(list_word_title)
            #print(all(item in list_word_title for item in list_word_search))
            # IF ALL WORDS FROM SEARCH ARE IN TITLE: RETURN

            if all(item in list_word_title for item in list_word_search):
                result_holder.append(comic)
    # ON FAILURE
    else:
        print('An error has occurred searching {}.'.format(shop))

    return result_holder
