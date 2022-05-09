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
    root.resizable(width=False, height=False)
    root.title("Podgląd oferty")
    # windows only (remove the minimize/maximize button)
    root.attributes('-toolwindow', True)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    
    response = requests.get(estate.get('zdjecie_glowne'), verify=False)

    imgLoad = Image.open(BytesIO(response.content))
    imgLoad.thumbnail((512, 512), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(imgLoad)

    photo = Label(root, image=render)
    photo.image = render
    photo.grid(column=0, row=0, columnspan=2, sticky=N)
    Label(root, text=estate.get("link")).grid(column=0, row=1, columnspan=2, sticky=N)

    for index, header in enumerate(estate):
        if (estate.get(header) != "-1" and not header in ["opis", "zdjecie_glowne", "zdjecia_linki", "zdjecie_glowne_link", "link"]):
            Label(root, text=header, anchor="w").grid(column=0, row=index + 2, sticky=N)
            Label(root, text=estate.get(header), anchor="w").grid(column=1, row=index + 2, sticky=N)

    opis = Text(root, height=10, width=50, wrap=WORD)
    opis.tag_configure('tag-center', justify='center')
    opis.grid(column=0, columnspan=2, row=index + 3, sticky=N)
    opis.insert(END, estate.get("opis"), 'tag-center')
    opis.config(state=DISABLED)


def showPhotoViewer(estate):
    root = Toplevel()
    root.title("Zdjęcia")
    root.currentIndex = 0
    # windows only (remove the minimize/maximize button)
    root.attributes('-toolwindow', True)
    showPhoto(estate, root)

    nextPhotoPartial = partial(nextPhoto, estate, root)
    prevPhotoPartial = partial(prevPhoto, estate, root)
    Button(root, text="Poprzednie", width=8, command=prevPhotoPartial).grid(column=0, row=1, sticky=N, pady=10)
    Button(root, text="Nastepne", width=8, command=nextPhotoPartial).grid(column=2, row=1, sticky=N, pady=10)


def showPhoto(estate, root):
    photoArray = estate.get('zdjecia_linki').replace('[', '').split(',')
    element = photoArray[root.currentIndex].replace("'", "")
    response = requests.get(element, verify=False)
    imgLoad = Image.open(BytesIO(response.content))
    imgLoad.thumbnail((528, 528), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(imgLoad)

    photo = Label(root, image=render)
    photo.image = render
    photo.grid(column=0, row=0, columnspan=3, sticky=N)
    Label(root, text=str(root.currentIndex + 1) + '/' + str(len(photoArray) - 1)).grid(column=1, row=1, sticky=N, pady=10)


def nextPhoto(estate, root):
    photoArray = estate.get('zdjecia_linki').replace('[', '').split(',')
    if root.currentIndex == len(photoArray) - 2:
        root.currentIndex = 0
    else:
        root.currentIndex += 1
    showPhoto(estate, root)


def prevPhoto(estate, root):
    photoArray = estate.get('zdjecia_linki').replace('[', '').split(',')
    if root.currentIndex == 0:
        root.currentIndex = len(photoArray) - 2
    else:
        root.currentIndex -= 1
    showPhoto(estate, root)


# create list of estates
def createList(container, estates, loader):
    sFrame = ScrollbarFrame(container, 650)
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

        showPhotoViewerPartial = partial(showPhotoViewer, estate)
        if estate.get('zdjecia_linki') != '-1':
            Button(frame, text="Zdjęcia", width=6, command=showPhotoViewerPartial).grid(column=8, row=id, sticky=N)
    loader.loaded()


def invalidateOffersFrame(container, loader):
    offersTable = createList(container, filteredOferList, loader)
    offersTable.grid(column=0, row=3, sticky=W, padx=5, pady=5)


def invalidateNewOffersFrame(container, loader):
    updatesTable = createList(container, newFilteredOfferList, loader)
    updatesTable.grid(column=1, row=3, sticky=W, padx=5, pady=5)
