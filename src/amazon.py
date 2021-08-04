import requests
from bs4 import BeautifulSoup
def amazon_search(search_string):
    """
    Search https://www.amazon.com.au/
    ONLY FROM AUSTRALIA DELIVERED WITH PRIME FREE DELIVERY
    """
    shop = "Amazon AU"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.amazon.com.au/s?k="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN Amazon THEY USE VOLUME INSTEAD OF VOL

    search_list = [x.lower() for x in search_list]
    if "vol" in search_list:
        search_list = [ "volume" if x=="vol" else x for x in search_list]

    full_search_url = base_search_url + separator.join(search_list) + \
                      "&i=stripbooks&rh=n%3A4893847051%2Cp_n_prime_domestic%3A6845356051%2Cp_n_free_shipping_eligible%3A5363790051&dc&qid=1627780271&rnid=5363788051&ref=sr_nr_p_n_free_shipping_eligible_1"

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
        list_of_products = soup.find_all('div',  src=lambda x: x and 'price' in x)

        list_of_products = [x for x in list_of_products if "result-item" in x["class"][0]]

        for article in list_of_products:

            if article.h2: # IF THERE IS A "DID yOU MEAN TYPO"

                comic_title = article.h2.text

                comic_url = "https://www.amazon.com.au" + article.find("a", class_ = "a-link-normal s-no-outline")["href"]

                # SPLITTING FOR WHEN IT HAS REDUCED PRICE TOO

                comic_price = article.find("span", class_ = "a-offscreen").text # IF NOT THERE IT'S UNAVAILABLE

                comic_price = float(comic_price.replace("$",""))

                comic = {"title": comic_title,
                         "url": comic_url,
                         "price": comic_price,
                         "shop":shop,
                         "availability": "In Stock"}

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
