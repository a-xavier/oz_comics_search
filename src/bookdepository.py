import requests
from bs4 import BeautifulSoup
def bookdepository_search(search_string):
    """
    Search https://www.bookdepository.com/
    Mostly UK based big shop
    """
    shop = "Bookdepository UK"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.bookdepository.com/search/?searchTerm="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN IMPACT COMICS THEY USE VOL INSTEAD OF VOLUME

    search_list = [x.lower() for x in search_list]
    if "volume" in search_list or "vol":
        search_list = [ "vol" if x=="volume" else x for x in search_list]

    
    full_search_url = base_search_url + separator.join(search_list) + "&ageRangesTotal=0&category=2633"
    #print(full_search_url)

    #GET WEB PAGE
    response = requests.get(full_search_url)

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response: # RESPONSE OK
        text_response = response.text
        soup = BeautifulSoup(text_response, 'html.parser')
        

        # GET ALL OBJECTS WITH CLASS=ARTICLE
        list_of_products = soup.find_all("div", class_ = "book-item")
        
        for article in list_of_products:
            comic_title = article.h3.text.strip()
            
            if article.find("p", class_ = "price"): # IF IT FINDS A PRICE IT'S AVAILABLE

                comic_url = "https://www.bookdepository.com" + article.a["href"]

                # SPLITTING FOR WHEN IT HAS REDUCED PRICE TOO

                comic_price = article.find("p", class_ = "price").get_text(strip=True).split("A$")[1] # IF NOT THERE IT'S UNAVAILABLE
                
                comic_price = float(comic_price)

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
                # REMOVE COLONS
                list_word_title = [x.replace(":","") for x in list_word_title]

                #print(list_word_search)
                #print(list_word_title)
                # IF ALL WORDS FROM SEARCH ARE IN TITLE: RETURN

                if all(item in list_word_title for item in list_word_search):
                    result_holder.append(comic)
    # ON FAILURE    
    else:
        print('An error has occurred searching {}.'.format(shop))

    return result_holder