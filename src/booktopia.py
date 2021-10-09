

import requests
from bs4 import BeautifulSoup
import ast
def booktopia_search(search_string):
    """
    Search https://www.booktopia.com.au/
    Big Chain
    """
    shop = "Booktopia"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.booktopia.com.au/search.ep?pn=1&productType=917504&keywords="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "%20"

    search_list = search_string.split(" ")

    #IN BOOKTOPIA THEY USE VOL INSTEAD OF VOLUME

    search_list = [x.lower() for x in search_list]
    if "vol" in search_list:
        search_list = [ "volume" if x=="vol" else x for x in search_list]


    full_search_url = base_search_url + separator.join(search_list) + "&cID=FX"

    #GET WEB PAGE
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                'referer': 'https://www.booktopia.com.au/'}
    response = requests.get(full_search_url, headers=headers)

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []


    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')

        # GET ALL OBJECTS WITH CLASS=ARTICLE
        #product
        list_of_products = soup.find_all("div", class_ ="product") #

        for article in list_of_products:
            comic_url = "https://www.booktopia.com.au" + article.a["href"]
            try:
                product_dict = ast.literal_eval(article.find("a", class_ = "buy-now button")["data-product-data"].replace("\n", " "))

                comic_title = product_dict["name"]

                comic_price = float(product_dict["price"])

                availability = product_dict["dimension1"]

                comic = {"title": comic_title,
                         "url": comic_url,
                         "price": comic_price,
                         "shop":shop,
                         "availability": availability}

                # DO SOME MATCHING
                # CRUDE = TAKE ALL 3+ LETTER WORDS IN SEARCH AND SEE IF THEY ARE IN COMIC TITLE
                list_word_search = [x.lower() for x in search_list if len(x)> 2]

                list_word_title = comic_title.split(" ")
                list_word_title = [x.lower() for x in list_word_title if len(x)> 2]
                # REMOVE COLONS
                list_word_title = [x.replace(":","") for x in list_word_title]
                list_word_title = [x.replace(";","") for x in list_word_title]
                list_word_title = [x.replace(",","") for x in list_word_title]
                list_word_title = [x.replace(".","") for x in list_word_title]
                list_word_title = [x.replace("(","") for x in list_word_title]
                list_word_title = [x.replace(")","") for x in list_word_title]

                #print(list_word_search)
                #print(list_word_title)
                # IF ALL WORDS FROM SEARCH ARE IN TITLE: RETURN
                if all(item in list_word_title for item in list_word_search):
                    if availability == "In-Stock":
                        result_holder.append(comic)
            except (TypeError, KeyError) as e:
                pass
    # ON FAILURE
    else:
        print('An error has occurred searching {}.'.format(shop))

    return result_holder
