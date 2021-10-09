
import requests
from bs4 import BeautifulSoup
def area_search(search_string):
    """
    Search https://area52.circlesoft.net/
    104 Elizabeth St, Hobart, Tasmania
    0362342322 or info@Area52.com.au
    ABN 806060078639 Area 52
    """
    shop = "Area 52"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://area52.circlesoft.net/catalog/search?utf8=%E2%9C%93&keyword="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN AREA 52 THEY USE BOTH VOL. AND VOLUME ?!
    #BETTER USE VOL

    search_list = [x.lower() for x in search_list]
    if "volume" in search_list:
        search_list = [ "vol" if x=="volume" else x for x in search_list]

    full_search_url = base_search_url + separator.join(search_list) + "&search_type=core%5Ekeyword"

    #print(full_search_url)

    #GET WEB PAGE
    response = requests.get(full_search_url, headers={"User-Agent":"Defined"})

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')

        acceptable_categories = ["Graphic Novels", "Indie Graphic Novels", "Young Adult Graphic Novels"]
        # GET ALL OBJECTS WITH CLASS=ARTICLE
        list_of_products = soup.find_all("div", class_="home-box featured-product product-list")

        for article in list_of_products:

            if article.p.a.text.strip() in acceptable_categories:

                comic_title = article.find("a", class_= "featured-product-header").text.strip()

                comic_url = "https://area52.circlesoft.net" + article.find("a", class_= "featured-product-header")["href"]

                # SPLITTING FOR WHEN IT HAS REDUCED PRICE TOO

                comic_price = article.h2.text.strip()

                comic_price = float(comic_price.replace("$","").replace("AUD",""))


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
