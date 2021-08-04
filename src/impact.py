import requests
from bs4 import BeautifulSoup
def impact_search(search_string):
    """
    Search https://impactcomics.com.au/
    16 Garema Pl, Canberra ACT 2601
    """
    shop = "Impact Comics"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://impactcomics.com.au/?s="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN IMPACT COMICS THEY USE VOL INSTEAD OF VOLUME

    search_list = [x.lower() for x in search_list]
    if "volume" in search_list or "vol":
        search_list = [ "vol" if x=="volume" else x for x in search_list]

    
    full_search_url = base_search_url + separator.join(search_list) + "&post_type=product"
    #print(full_search_url)

    #GET WEB PAGE
    response = requests.get(full_search_url)

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')
        

        # GET ALL OBJECTS WITH CLASS=ARTICLE
        list_of_products = soup.find_all("a", class_ = "woocommerce-LoopProduct-link woocommerce-loop-product__link")
        
        for article in list_of_products:
            comic_title = article.h2.text

            if comic_title: # IF TITLE NOT EMPTY

                comic_url =article["href"]

                comic_price = article.bdi.text
                
                comic_price = float(comic_price.replace("$", ""))

                availability = article.p.text

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

                #print(list_word_search)
                #print(list_word_title)
                # IF ALL WORDS FROM SEARCH ARE IN TITLE: RETURN
                if all(item in list_word_title for item in list_word_search):
                    if availability == "In stock":
                        result_holder.append(comic)
    # ON FAILURE    
    else:
        print('An error has occurred searching {}.'.format(shop))

    return result_holder
