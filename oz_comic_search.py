"""
SCRIPT TO SEARCH ALL AUSTRALIAN COMIC BOOK SHOPS with online stores
Simply input search terms and get Title | Price | Link for all shops
"""
from src.comicsetc import comic_etc_search
from src.secrethq import secrethq_search
from src.incognito import incognito_search
from src.allstar import allstar_search
from src.impact import impact_search
from src.bookdepository import bookdepository_search
from src.amazon import amazon_search
from src.booktopia import booktopia_search
from src.comicsrus import comicsrus_search
from src.popcultcha import pop_cultcha_search
from src.macs import macs_search
from src.area52 import area_search
from src.minotaur import minotaur_search
from src.greenlight import greenlight_search


from src.filtering import filtering_results
from sys import exit
import argparse



if __name__ == "__main__":
    print(amazon_search("the walking dead"))
    """
    parser = argparse.ArgumentParser(description='Search Comics from Australian Comic Book Stores')
    parser.add_argument('term', metavar='Search Term', type=str,
                    help='The search term')
    parser.add_argument('-b', metavar='Kind of book', type=str, default=None,
                    help='Kind of book, can be either Nothing, trade or issue')
    parser.add_argument('-n', metavar='Book number', type=int, default=None,
                    help='Issue / Volume number, int')

    args = parser.parse_args()

    search_term = args.term

    print("#"*40 + "\nSearching for: {} \n".format(search_term)+ "#"*40)

    results = comic_etc_search(search_term) + secrethq_search(search_term) \
                   + incognito_search(search_term) + allstar_search(search_term) \
                   + impact_search(search_term) + bookdepository_search(search_term) \
                   + amazon_search(search_term) + booktopia_search(search_term) \
                   + pop_cultcha_search(search_term) + comicsrus_search(search_term) \
                   + macs_search(search_term) + area_search(search_term) \
                   + minotaur_search(search_term) + greenlight_search(search_term)

    results = filtering_results(results, args.b, args.n)
    if len(results) == 0:
        print("No result found!\nTry playing around with filtering / search terms")
    else:
        for item in results:
            print(item["shop"].upper())

            for key, value in item.items():
                if key != "shop":
                    print(key + ": " + str(value))
            print("------------")
"""
