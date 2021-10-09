import requests
from bs4 import BeautifulSoup
def macs_search(search_string):
    """
    Search https://www.macscomics.com.au/
    Email Us
    sales@macscomics.com.au
    Location
    Shop 2/34 Sydney Street Mackay QLD
    """
    shop = "Mac's Comics"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.macscomics.com.au/search?q="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN MACS COMICS THEY USE VOL INSTEAD OF VOLUME

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

        for article in soup.find_all("div", class_="row results"):
            comic_title = article.h3.text
            comic_url = "https://www.macscomics.com.au" + article.h3.a["href"]
            # HAS TO FIND PRICE ON ANOTHER PAGE
            price_text = requests.get(comic_url, headers={"User-Agent":"Defined"}).text
            comic_price = BeautifulSoup(price_text, 'html.parser').find("h2", class_="price").text
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
