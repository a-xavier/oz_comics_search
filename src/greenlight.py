import requests
from bs4 import BeautifulSoup
def greenlight_search(search_string):
    """
    Search https://greenlightcomics.com/
    feel free to message us
    https://www.facebook.com/greenlightcomics/
    https://www.instagram.com/greenlightcomics
    we even have a phone!
    08 8231 1150
    Or Send Us An Email!
    read@greenlightcomics.com
    """
    shop = "Greenlight Comics"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://greenlightcomics.com/?s="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN Greenligh Comics THEY USE VOL INSTEAD OF VOLUME

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

        list_of_products = soup.find_all("div", class_="elementor-post__card")

        for article in list_of_products:

            if not article.find("div", class_="elementor-post__badge"): # IF THERE IS THAT, IT'S A PREVIEW / OTHER ARTICLE
                comic_title = article.h3.text.strip()

                comic_url =  article.a["href"]

                # SINCE THEY DON'T SHOW THE PRICE ON THE SEARCH PAGE
                # GOT TO CHECK INDIVIDUAL PAGES

                r = requests.get(comic_url, headers={"User-Agent":"Defined"})
                if r:
                    book_soup = BeautifulSoup(r.text, 'html.parser')

                    if not book_soup.find("p", class_="stock out-of-stock"): # IT IT'S THERE IT'S OUT OF STOCK:

                        comic_price = book_soup.find("p", class_="price").text.strip()

                        comic_price = float(comic_price.replace("$","").replace("AUD",""))

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
                else:
                    print('An error has occurred searching {}.'.format(shop))
    # ON FAILURE
    else:
        print('An error has occurred searching {}.'.format(shop))

    return result_holder
