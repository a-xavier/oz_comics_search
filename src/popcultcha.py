
import requests
from bs4 import BeautifulSoup
def pop_cultcha_search(search_string):
    """
    Old Griffiths Bookstore
    96-98 Ryrie Street
    Geelong, VIC, 3220
    Australia

    1300 586 293

    West 3, 13-35 Mackey St.
    North Geelong, VIC, 3215
    Australia

    1300 586 292

    +61 3 5240 7979
    Mon - Fri, 9am - 5:30pm (AEST)

    """
    shop = "PopCultcha"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.popcultcha.com.au/catalogsearch/result/index/?cat=21855&q="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN POPCULTCHA THEY USE VOLUME INSTEAD OF VOL

    search_list = [x.lower() for x in search_list]
    if "vol" in search_list:
        search_list = [ "volume" if x=="vol" else x for x in search_list]

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
        list_of_products = soup.find_all("li", class_="item product product-item")

        for article in list_of_products:

            comic_title = article.find("a" ,class_="product-item-link").text.strip()

            comic_url = article.find("a" ,class_="product-item-link")["href"]

            # SPLITTING FOR WHEN IT HAS REDUCED PRICE TOO

            comic_price = article.find("span", class_="price").text

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
            list_word_title = [x.replace(",","") for x in list_word_title]

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
