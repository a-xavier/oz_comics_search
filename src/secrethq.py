import requests
from bs4 import BeautifulSoup
def secrethq_search(search_string):
    """Search https://secrethqcomics.com.au/
     3/2 Beaconsfield-Emerald Rd, Beaconsfield VIC 3807
    """
    shop = "Secret HQ Comics"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://secrethqcomics.com.au/search?q="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN SHQC THEY USE VOL INSTEAD OF VOLUME

    search_list = [x.lower() for x in search_list]
    if "volume" in search_list:
        search_list = [ "vol" if x=="volume" else x for x in search_list]

    full_search_url = base_search_url + separator.join(search_list)
    #print(full_search_url)

    #GET WEB PAGE
    response = requests.get(full_search_url)

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')

        # GET ALL OBJECTS WITH CLASS=ARTICLE
        list_of_products = soup.find_all('div', class_='product-index desktop-3 mobile-half') + soup.find_all('div', class_='product-index desktop-3 mobile-half first')

        #print(list_of_products)

        for article in list_of_products:
            comic_title = article.span.text.strip()

            comic_url = "https://secrethqcomics.com.au"+ article.a["href"]
            try:
                comic_price = article.find("div", class_="prod-price").text
            except AttributeError: # NONETYPE HAS NO ATTRIBUTE TEXT HAPPEN IF SALE
                comic_price = article.find("div", class_="onsale").text
            comic_price = float(comic_price.replace("$", ""))

            if not article.find("div", class_="so icn"):
                availability = "In Stock"
            else:
                availability = "Sold Out"

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
                if availability == "In Stock":
                    result_holder.append(comic)



    # ON FAILURE
    else:
        print('An error has occurred searching Secret HQ Comics.')

    return result_holder
