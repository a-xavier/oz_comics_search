"""
GUI Version of Oz_comic_search
SCRIPT TO SEARCH ALL AUSTRALIAN COMIC BOOK SHOPS with online stores
Simply input search terms and get Title | Price | Link for all shops
"""

from tkinter import *  # FOR GUI
from tkinter import ttk
from PIL import ImageTk,Image

#MULTITHREADING
from threading import Thread


#ALL SEARCH FUNCTIONS
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

#FILTERING
from src.filtering import filtering_results
#MISC
from sys import exit
from pandas import DataFrame
from webbrowser import open
from sys import platform

# GLOBAL THAT WILL HOLD THE FINAL filtering_results
final_result = []

##### DEFINE MAIN ######

def main():
    global final_result
    # COLLECTION OF SEARCHED
    not_evil_search = [comic_etc_search, secrethq_search, incognito_search, \
    allstar_search, impact_search, comicsrus_search, pop_cultcha_search, \
    macs_search, area_search, minotaur_search, greenlight_search]

    evil_search = [comic_etc_search, secrethq_search, incognito_search, \
    allstar_search, impact_search, comicsrus_search, pop_cultcha_search, \
    macs_search, area_search, minotaur_search, greenlight_search, \
    bookdepository_search, booktopia_search, amazon_search]


    ############## START PROCESS OPTIONS ################

    # CONTEXT MENU
    def make_textmenu(root):
        global the_menu
        the_menu = Menu(root, tearoff=0)
        the_menu.add_command(label="Cut")
        the_menu.add_command(label="Copy")
        the_menu.add_command(label="Paste")
        the_menu.add_separator()
        the_menu.add_command(label="Select all")

    def callback_select_all(event):
        # select text after 50ms
        root.after(50, lambda:event.widget.select_range(0, 'end'))

    def show_textmenu(event):
        e_widget = event.widget
        the_menu.entryconfigure("Cut",command=lambda: e_widget.event_generate("<<Cut>>"))
        the_menu.entryconfigure("Copy",command=lambda: e_widget.event_generate("<<Copy>>"))
        the_menu.entryconfigure("Paste",command=lambda: e_widget.event_generate("<<Paste>>"))
        the_menu.entryconfigure("Select all",command=lambda: e_widget.select_range(0, 'end'))
        the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)



    def launch_threaded(func):
        global final_result
        Thread(target = func, daemon=True).start()

    def open_link(a):
        curItem = result_field.focus()
        try:
            url_to_open = result_field.item(curItem)["values"][1]
            print(url_to_open)
            open(url_to_open)
        except IndexError:
            pass

    def click_search(event=None):
        global final_result

        # CHECK IF ISSUE/VOL IS NUMERIC
        try:
            volume_argument = int(vol_selector.get()) # THERE IS A VOLUME AND IT IS A NUMBER
        except ValueError:
            if vol_selector.get() == "": # THERE IS NOTHING IN THE BOX:
                volume_argument = 0
            else:     # THERE IS TEXT IN THERE
                status_label_text.set("Volume / Issue MUST be a number")
                status_label.config(text=status_label_text.get())
                return # STOP HERE

        if search_term.get() == "": # IF NOTHING IN SEARCH BAR
            return

        final_result = [] # RESET EVERY NEW SEARCH
        #DEACTIVATE EVERYTHING
        search_bar["state"] = DISABLED
        search_button["state"] = DISABLED
        type_listbox["state"] = DISABLED
        volume_entry["state"] = DISABLED
        evil_checkbutton["state"] = DISABLED

        status_label_text.set("LOOKING FOR COMICS")
        status_label.config(text=status_label_text.get())

        # GET ALL PARAMETERS
        #search_term.set("old man hawkeye")
        search_term_argument = search_term.get()

        type_argument = type_selector.get()
        evil_argument = evil_selector.get()

        # PROCESS ARGUMENTS:
        if volume_argument == 0:
            volume_argument = None

        if type_argument == "":
            type_argument = None

        print("ARGUMENTS ARE : {} | {} | {} | {}".format(search_term_argument,type_argument, volume_argument, evil_argument))

        if evil_argument == True:
            list_of_shops = evil_search
        else:
            list_of_shops = not_evil_search

        final_result_holder = []
        thread_list = []

        # MULTITHREADING ?
        def threaded_search(shop_search_function, search_term, result_holder):
            final_result_holder.append(shop_search_function(search_term))

        for shop_function_search in list_of_shops:
            #print(shop_function_search)
            #print("Creating Threads")
            #print(search_term_argument)

            t = Thread(target=threaded_search, args=(shop_function_search,search_term_argument,final_result_holder))
            thread_list.append(t)

        #print(thread_list)
        #print(len(thread_list))
        for search_thread in thread_list:
            print("Starting_thread {}".format(search_thread))
            search_thread.start()

        for search_thread in thread_list:
            print("WAIT FOR FINISH {}".format(search_thread))
            search_thread.join()
        final_result = [item for sublist in final_result_holder for item in sublist if sublist != []]

        if volume_argument or type_argument:
            final_result = filtering_results(final_result, type_argument, volume_argument)
        # REORDER
        final_result = sorted(final_result, key=lambda k: k['price'])

        ### PRINT RESULTS ####

        print_df = DataFrame.from_dict(final_result)
        print(print_df)
        # TRY Treeview

        #delete previous Treeview
        result_field.delete(*result_field.get_children())

        for i in range(len(print_df.index.values)):
            result_field.insert('','end',value=tuple(print_df.iloc[i].values))
        # columns = ["title", "url", "price", "shop", "availability"]
        result_field.column("title",width=200,anchor='center')
        result_field.column("url",width=100, anchor="center")
        result_field.column("price",width=150, anchor="center")
        result_field.column("shop",width=150, anchor="center")
        result_field.column("availability",width=150, anchor="center")

        result_field.heading("title",text="Title")
        result_field.heading("url",text="URL")
        result_field.heading("price",text="Price")
        result_field.heading("shop",text="Shop")
        result_field.heading("availability",text="Availability")

        vsb = ttk.Scrollbar(root, orient="vertical", command=result_field.yview)
        result_field.configure(yscrollcommand=vsb.set)
        vsb.grid(column=7, row = 1, rowspan = 20, sticky=E+S+N)

        result_field.bind('<Double-Button-1>', open_link)


        #ARCITAVE EVERYTHING
        search_bar["state"] = NORMAL
        search_button["state"] = NORMAL
        type_listbox["state"] = "readonly"
        volume_entry["state"] = NORMAL
        evil_checkbutton["state"] = NORMAL

        status_label_text.set("DONE")
        status_label.config(text=status_label_text.get())

    ##############  END PROCESSING OPTIONS################

    # COLOR SETUP
    bg_left = "light grey"
    bg_rigt = "black"

    # SETUP BASICS FOR GUI
    root = Tk() # ROOT IS TOP LEVEL WINDOW
    root.configure(background=bg_left)
    root.title("Oz Comics Search") # TITLE OF THE WINDOW
    root.minsize(600,300)
    #TODO ADD iCON THAT WORKS
    try:
        root.iconbitmap( 'icon.ico')
    except TclError:
        pass
    #root.geometry("1080x600") # SIZE AT STARTUP

    make_textmenu(root)

    # bind the feature to all Entry widget
    if platform == "darwin":
        root.bind_class("Entry", "<Button-2><ButtonRelease-2>", show_textmenu)
        root.bind_class("Entry", "<Control-a>", callback_select_all)

    else:
        root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
        root.bind_class("Entry", "<Control-a>", callback_select_all)



    # LEFT PANEL
############## START LEFT OPTIONS ################
    #creates a frame that is a child of object named 'root'
    left_frame = Frame(master=root, bg=bg_left, relief = "raised")
    left_frame.grid(row = 1, column = 1)


    ##### SETUP ALL VARIABLES  #####

    type_selector = StringVar() # STORE VALUE OF TYPE SELECTION
    vol_selector = StringVar() # STORE VALUE OF VOLUME SELECTION
    evil_selector = BooleanVar() # STORE VALUE OF EVIL ON/OFF
    search_term = StringVar() #IS THE ACTUAL SEARCH TERM


    # LOGO ROW = 1
    try:
        canvas = Canvas(left_frame, width = 300, height = 100, bg = bg_left)
        canvas.grid(row=1, column=1, columnspan=2)
        img = PhotoImage(file="src/logo.png")
        canvas.create_image(0,0, anchor=NW, image=img)
    except TclError:
        canvas.create_text(150,50,text = "Oz Comics Search", justify = CENTER, font = 'Helvetica 24')

    # LABEL ROW = 2
    search_label = Label(left_frame, text="Search for trade, issue, graphic novels...", bg = bg_left)
    search_label.grid(row = 2, column = 1)


    # SEARCH ROW = 3
    search_row = 3
    # SEARCH BAR: ENTRY
    search_bar = Entry(left_frame, textvariable = search_term)
    search_bar.grid(row=search_row,column=1, padx = 0, columnspan=2, sticky = W+E)

    # SEARCH BUTTON: BUTTON
    search_button = Button(left_frame, text = "Search", bg = bg_left, command = lambda: launch_threaded(click_search))
    search_button.grid(row=search_row+1,column=1,columnspan=2)

    # OPTION LABEL ROW = 5
    option_row = 5
    type_label = Label(left_frame, text= "Choose Book Type", bg = bg_left)
    type_label.grid(row=option_row,column=1)

    volume_label = Label(left_frame, text= "Volume / Issue #", bg = bg_left)
    volume_label.grid(row=option_row,column=2)

    # OPTION ROW = 6
    option_row = 6

    #TYPE SELECTOR = COMBOBOX
    type_selector = StringVar()
    type_list = ["", "trade", "issue"]
    type_listbox = ttk.Combobox(left_frame, cursor = "hand2", justify = CENTER, textvariable=type_selector, state="readonly")
    type_listbox['values'] = type_list
    type_listbox.grid(row = option_row, column = 1)

    # VOLUME SELECTOR = Entry
    volume_entry = Entry(left_frame, textvariable = vol_selector)
    volume_entry.grid(row=option_row,column=2)

    # Check Button evil mode
    check_evil_row = 7
    evil_checkbutton = Checkbutton(left_frame, bg = bg_left, variable = evil_selector, onvalue = True, offvalue = False)
    evil_checkbutton.grid(row = check_evil_row, column = 1, sticky = E)

    evil_label = Label(left_frame, text="Include Amazon AU, Bookdepository, Booktopia", bg = bg_left)
    evil_label.grid(row = check_evil_row, column = 2)

    # STATUS LABEL
    status_label_text = StringVar()
    status_label = Label(left_frame, text = status_label_text.get(), bg = bg_left)
    status_label.grid(row = check_evil_row + 1, column=1, columnspan=2)

############## END LEFT OPTIONS ################

    search_bar.bind('<Return>', lambda event, func = click_search: launch_threaded(func))


############## START RIGHT RESULTS ################

    #creates a frame that is a child of object named 'root'
    #right_frame = Frame(master=root, bg=bg_rigt, relief = "raised")
    #right_frame.grid(column = 3, row = 1, columnspan=4, rowspan=15, sticky=W+E+N+S)
    columns = ["title", "url", "price", "shop", "availability"]
    result_field = ttk.Treeview(master=root,show="headings", columns=columns)
    result_field.grid(column = 3, row = 1, columnspan=1, rowspan = 5 ,sticky=W+E+S+N)
    root.columnconfigure(3,weight=1)
    root.rowconfigure(5,weight=1)
############## END RIGHT RESULTS ################


    ###### RUN ######
    root.mainloop()


if __name__ == '__main__':
    main()
