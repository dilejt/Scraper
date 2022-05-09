from tkinter import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PIL import Image, ImageTk
from io import BytesIO
from ScrollbarFrame import ScrollbarFrame
from functools import partial
import re
from consts import filteredOferList, offersList, newFilteredOfferList
from threading import Thread

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def validate(string):
    regex = re.compile(r"(\+|\-)?[0-9,]*$")
    result = regex.match(string)
    return (string == ""
            or (string.count('+') <= 1
                and string.count('-') <= 1
                and string.count(',') <= 1
                and result is not None
                and result.group(0) != ""))


def onValidate(P):
    return validate(P)


def addValidateOnInput(entry):
    entry.config(validatecommand=(entry.register(onValidate), '%P'))


# create window with additional estate data
def initExtraInformationGui(estate):
    root = Toplevel()
    root.title("nr oferty")

    # windows only (remove the minimize/maximize button)
    root.attributes('-toolwindow', True)

    response = requests.get(estate.get('zdjecie_glowne'), verify=False)
    imgLoad = Image.open(BytesIO(response.content))
    imgLoad.thumbnail((528, 528), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(imgLoad)

    photo = Label(root, image=render)
    photo.image = render
    photo.grid(column=0, row=0, columnspan=2, sticky=N)


# create list of estates
def createList(container, estates, loader):
    sFrame = ScrollbarFrame(container)
    frame = sFrame.scrolled_frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=3)

    Thread(target=lambda: appendData(estates, frame, loader)).start()
    return sFrame


def appendData(estates, frame, loader):
    for id, estate in enumerate(estates):
        response = requests.get(estate.get('zdjecie_glowne'), verify=False)
        try:
            imgLoad = Image.open(BytesIO(response.content))
            imgLoad.thumbnail((58, 58), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(imgLoad)
            photo = Label(frame, image=render)
            photo.image = render
            photo.grid(column=0, row=id, columnspan=2, sticky=N)
        except:
            print("Temp img didn't find")

        # Associate img with label & alocate in grid

        Label(frame, text=estate.get('typ')).grid(column=2, row=id, sticky=N)
        Label(frame, text=estate.get('cena')).grid(column=3, row=id, sticky=N)
        Label(frame, text=estate.get('lokalizacja')).grid(column=4, row=id, sticky=N)
        Label(frame, text=estate.get('rynek')).grid(column=5, row=id, sticky=N)
        Label(frame, text=estate.get('biuro')).grid(column=6, row=id, sticky=N)
        action_with_arg = partial(initExtraInformationGui, estate)
        Button(frame, text="Zobacz", width=8, command=action_with_arg).grid(column=7, row=id, sticky=N)
    loader.loaded()


def invalidateOffersFrame(container, loader):
    offersTable = createList(container, filteredOferList, loader)
    offersTable.grid(column=0, row=3, sticky=W, padx=5, pady=5)


def invalidateNewOffersFrame(container, loader):
    updatesTable = createList(container, newFilteredOfferList, loader)
    updatesTable.grid(column=1, row=3, sticky=W, padx=5, pady=5)
