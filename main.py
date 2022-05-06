from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO
from ScrollbarFrame import ScrollbarFrame
from functools import partial
from tkinter.ttk import Treeview
from consts import OFFICE_PROPERTY
from buttonMethods import generateOnClickHandler


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.root.title("Scrapers")
        self.initMainGui()
        mainloop()

    def initMainGui(self):
        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(1, weight=5)
        self.root.columnconfigure(2, weight=2)

        offers_label = Label(self.root, text="Oferty")
        offers_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        # Begining of filter frame
        filter_frame = Frame(self.root)

        offers_filter_input = Entry(offers_filter_frame, width=40)
        offers_filter_input.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        offers_filter_variable = StringVar(offers_filter_frame)
        offers_filter_variable.set("typ")
        offers_option_menu = OptionMenu(offers_filter_frame, offers_filter_variable, "typ", "cena", "biuro",
                                        "lokalizacja", "powierzchnia")
        offers_option_menu.config(width=7)
        offers_option_menu.grid(column=1, row=0, sticky=N, padx=5, pady=5)

        offers_files_btn = Button(offers_filter_frame, text="Filtruj")
        offers_files_btn.grid(column=2, row=0, sticky=W, padx=5, pady=5)

        offers_filter_frame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        updates_filter_frame = Frame(self.root)

        updates_filter_input = Entry(updates_filter_frame, width=40)
        updates_filter_input.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        filter_frame.grid(column=0, row=1, sticky=W, padx=5, pady=5)
        # End of filter frame
        updates_filter_variable = StringVar(updates_filter_frame)
        updates_filter_variable.set("typ")
        updates_option_menu = OptionMenu(updates_filter_frame, updates_filter_variable, "typ", "cena", "biuro",
                                         "lokalizacja", "powierzchnia")
        updates_option_menu.config(width=7)
        updates_option_menu.grid(column=1, row=0, sticky=N, padx=5, pady=5)

        updates_files_btn = Button(updates_filter_frame, text="Filtruj")
        updates_files_btn.grid(column=2, row=0, sticky=W, padx=5, pady=5)

        updates_filter_frame.grid(column=1, row=1, sticky=W, padx=5, pady=5)

        # Begining of lists todo dodac jako 2 parametr zassane dane z global csv'ki
        offers_table = create_list(self.root, [])
        offers_table.grid(column=0, row=2, sticky=W, padx=5, pady=5)

        updates_table = create_list(self.root, [])
        updates_table.grid(column=1, row=2, sticky=W, padx=5, pady=5)
        # End of lists

        # Begining of button frame
        button_frame = Frame(self.root)

        variable = StringVar(button_frame)
        variable.set(OFFICE_PROPERTY['landowscy'])
        option_menu = OptionMenu(button_frame, variable, *OFFICE_PROPERTY.values())
        option_menu.config(width=7)
        option_menu.grid(column=0, row=0, sticky=N, padx=5, pady=5)

        generate_btn = Button(button_frame, text="Generuj", width=10, command=lambda: generateOnClickHandler(variable.get()))
        generate_btn.grid(column=0, row=1, sticky=N, padx=5, pady=5)

        merge_btn = Button(button_frame, text="Łączenie", width=10)
        merge_btn.grid(column=0, row=2, sticky=N, padx=5, pady=5)

        files_btn = Button(button_frame, text="Pliki...", width=10)
        files_btn.grid(column=0, row=3, sticky=N, padx=5, pady=5)

        button_frame.grid(column=2, row=2, sticky=N, padx=5, pady=5)
        # End of button frame

# create window with additional estate data
def initExtraInformationGui(estate):
    root = Toplevel()
    root.title("nr oferty")

    # windows only (remove the minimize/maximize button)
    root.attributes('-toolwindow', True)

    directory = Path.cwd() / "photos"
    img = directory / estate.zdjecie_glowne

    response = requests.get("https://media-exp1.licdn.com/dms/image/C5603AQHbhjaf38qzVA/profile-displayphoto-shrink_800_800/0/1615299021631?e=1657152000&v=beta&t=jEKYS5YrkiPgQ5OI8X7G4kgu_WclnX5TumntYiqIKPE")
    imgLoad = Image.open(BytesIO(response.content))
    imgLoad.thumbnail((528, 528), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(imgLoad)

    photo = Label(root, image=render)
    photo.image = render
    photo.grid(column=0, row=0, columnspan=2, sticky=N)

# create list of lukaszek
def create_list(container, data):
    global action_with_arg, action_with_arg
    sFrame = ScrollbarFrame(container)
    frame = sFrame.scrolled_frame

    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)
    for id in range(6):
        # render img
        response = requests.get(
            "https://media-exp1.licdn.com/dms/image/C5603AQHbhjaf38qzVA/profile-displayphoto-shrink_800_800/0/1615299021631?e=1657152000&v=beta&t=jEKYS5YrkiPgQ5OI8X7G4kgu_WclnX5TumntYiqIKPE")
        imgLoad = Image.open(BytesIO(response.content))
        imgLoad.thumbnail((128, 128), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(imgLoad)

        # associate img with label & alocate in grid
        photo = Label(frame, image=render)
        photo.image = render
        photo.grid(column=0, row=id, columnspan=2, sticky=N)

        Label(frame, text="typ").grid(column=3, row=id, sticky=N)
        Label(frame, text="nr oferty").grid(column=4, row=id, sticky=N)
        action_with_arg = partial(initExtraInformationGui, [])  # todo dodac do partiala obiekt/dictionary z ofertą
        Button(frame, text="Zobacz", width=8, command=action_with_arg).grid(column=5, row=id, sticky=N)

    # for id, estate in enumerate(newEstates):  todo zdecydowac czy  odczytujemy z csv obiektowo czy jako dictionary - tutaj odpowiedz obiektowa
    #     objEstate = newEstates.get(estate)
    #     directory = Path.cwd() / "photos"
    #      response = requests.get(objEstate.zdjecie_glowne)
    #
    #      imgLoad = Image.open(BytesIO(response.content))
    #      imgLoad.thumbnail((128, 128), Image.ANTIALIAS)
    #      render = ImageTk.PhotoImage(imgLoad)
    #      # associate img with label & alocate in grid
    #      photo = Label(frame, image=render)
    #      photo.image = render
    #      photo.grid(column=0, row=id, columnspan=2, sticky=N)
    #     ttk.Label(frame, text=objEstate.typ).grid(column=3, row=id, sticky=tk.N)
    #     ttk.Label(frame, text=objEstate.nr_oferty).grid(column=4, row=id, sticky=tk.N)
    #     action_with_arg = partial(create_details_window, objEstate)
    #     ttk.Button(frame, text="Zobacz", width=8, command=action_with_arg).grid(column=5, row=id, sticky=tk.N)
    #

    return sFrame

if __name__ == '__main__':
    MainFrame()
