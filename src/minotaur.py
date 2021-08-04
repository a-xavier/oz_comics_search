
import requests
from bs4 import BeautifulSoup
def minotaur_search(search_string):
    """
    Search https://www.minotaur.com.au/
    Minotaur Entertainment  	  Phone: +61 3 9670  5414
    264 Little Collins Street	  Comics: +61 3 9670  5415
    Melbourne, 3000, Australia
 	 For enquiries about existing web orders: web@minotaur.com.au
     For general stock enquiries & other issues: sales@minotaur.com.au
    """
    shop = "Minotaur"

    # ROOT OF URL FOR SEARCH
    base_search_url = "https://www.minotaur.com.au/site.asp?action=search&keywords="

    # TERM THAT SEPARATE WORDS FOR SEARCH
    separator = "+"

    search_list = search_string.split(" ")

    #IN MINOTAUR THEY USE VOL and not VOLUME ?!

    search_list = [x.lower() for x in search_list]
    if "volume" in search_list:
        search_list = [ "vol" if x=="volume" else x for x in search_list]

    # DO 2 SEARCH FOR GRAPHIC NOVELS AND FOR SINGLE ISSUES
    gn_url = base_search_url + separator.join(search_list) + "&titleauthor=all&searchpreviews=++&ptypetheme=ptype1026&submit.x=0&submit.y=0"
    issue_url = base_search_url + separator.join(search_list) + "&titleauthor=all&searchpreviews=++&ptypetheme=ptype1003&submit.x=0&submit.y=0"

    #GN URL SHOW DIRECT RESULTS BUT ISSUE ONLY SHOWS A LINK WITH NO PRICE AT all

    #print(full_search_url)
######################## GRAPHIC NOVELS
    #GET WEB PAGE
    response_gn = requests.get(gn_url, headers={"User-Agent":"Defined"})

    # RETURN OBJECT IS A LIST OF DICT
    result_holder = []

    if response_gn: # RESPONSE OK
        text_response_gn = response_gn.text
        soup_gn = BeautifulSoup(text_response_gn, 'html.parser')

        # GET ALL OBJECTS WITH CLASS=ARTICLE
        list_of_products_gn = soup_gn.find_all("td", class_="Content")

        for article in list_of_products_gn:
            comic_title = article.a.text.strip()

            comic_url = "https://www.minotaur.com.au/" + article.a["href"]

            # SPLITTING FOR WHEN IT HAS REDUCED PRICE TOO

            comic_price = article.b.text.strip()

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
            list_word_title = [x.replace(",","") for x in list_word_title]

            #print(list_word_search)
            #print(list_word_title)
            #print(all(item in list_word_title for item in list_word_search))
            # IF ALL WORDS FROM SEARCH ARE IN TITLE: RETURN

            if all(item in list_word_title for item in list_word_search):
                result_holder.append(comic)
################### SINGLE ISSUES ################
    #GET WEB PAGE
    response_issue = requests.get(issue_url, headers={"User-Agent":"Defined"})

    if response_issue: # RESPONSE OK
        text_response_issue = response_issue.text
        soup_issue = BeautifulSoup(text_response_issue, 'html.parser')


        # GET ALL OBJECTS WITH CLASS=ARTICLE
        product_list_issue = soup_issue.find_all("td", class_="Content")

        for article in product_list_issue:
            comic_url = "https://www.minotaur.com.au/" + article.a["href"]
            r =  requests.get(comic_url, headers={"User-Agent":"Defined"})
            if r:
                 issue_soup = BeautifulSoup(r.text, 'html.parser')

                 article = issue_soup.find("meta", attrs={"content":"product", "property":"og:type"})

                 comic_title = article.find("div", class_ = "LargeText").text.strip()

                 comic_price = article.font.text.strip()
                 comic_price = float(comic_price.replace("$", ""))

                 if issue_soup.find("font", attrs={"color":"red"}): # IF THIS EXIST THERE IS NO STOCK
                     availability = "Out of stock"
                 else:
                     availability = "In Stock"

            else:
                pass

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
                if availability == "In Stock":
                    result_holder.append(comic)



    # ON FAILURE
    else:
        print('An error has occurred searching {}.'.format(shop))

    return result_holder
