def filtering_results(results, book_type, number):
    """
    results = list of dictionnary
    Filter the results to getspecific type trade / issue
    include omnibus and compendium in trades
    and number

    Based on comic title
    """
    assert book_type in ["trade", "issue", None] , "Choose between 'trade' or 'issue' or leave blank (compendium and omnibus are trades)"

    type_filtered_holder = []
    number_filtered_holder = []# Will hold the new entries after filtering step
    # FIRST GET EITHER ISSUE OR PAPERBACK ADD TYPE
    paperback_signs = ["vol", "vol.", "volume", "tpb", 'pb',"tp", "paperback" ,"omnibus", "compendium", "hc", "hardcover", "graphic novel", "softcover"]
    issue_signs = ["#"]

    for book in results:
        if any(x in book["title"].lower() for x in paperback_signs):
            book["type"] = "trade"
        elif any(x in book["title"].lower() for x in issue_signs):
            book["type"] = "issue"
        else:
            book["type"] = "unknown (assume trade)"

    if book_type: # NOT NONE
        for book in results:
            if book["type"] == book_type or book["type"] == "unknown (assume trade)":
                type_filtered_holder.append(book)
    else:
        type_filtered_holder = results

    if number:
        for book in type_filtered_holder:
            if "{}".format(number) in book["title"] or "0{}".format(number) in book["title"]:
                number_filtered_holder.append(book)
    else:
        number_filtered_holder = type_filtered_holder

    # PUT CHEAPER FIRST

    number_filtered_holder = sorted(number_filtered_holder, key=lambda k: k['price'])

    return number_filtered_holder
