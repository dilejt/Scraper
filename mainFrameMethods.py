from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO
from ScrollbarFrame import ScrollbarFrame
from functools import partial
import re


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

    response = requests.get(estate.get('zdjecie_glowne'))
    imgLoad = Image.open(BytesIO(response.content))
    imgLoad.thumbnail((528, 528), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(imgLoad)

    photo = Label(root, image=render)
    photo.image = render
    photo.grid(column=0, row=0, columnspan=2, sticky=N)


# create list of estates
def createList(container, estates):
    sFrame = ScrollbarFrame(container)
    frame = sFrame.scrolled_frame

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=3)

    for id, estate in enumerate(estates):
        response = requests.get(estate.get('zdjecie_glowne'))
        try:
            imgLoad = Image.open(BytesIO(response.content))
            imgLoad.thumbnail((58, 58), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(imgLoad)
            photo = Label(frame, image=render)
            photo.image = render
            photo.grid(column=0, row=id, columnspan=2, sticky=N)
        except:
            print("temp img didn't find")

        # Associate img with label & alocate in grid

        Label(frame, text=estate.get('typ')).grid(column=3, row=id, sticky=N)
        Label(frame, text=estate.get('nr_oferty')).grid(column=4, row=id, sticky=N)
        action_with_arg = partial(initExtraInformationGui, estate)
        Button(frame, text="Zobacz", width=8, command=action_with_arg).grid(column=5, row=id, sticky=N)

    return sFrame
