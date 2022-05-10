import csv
import tkinter, tkinter.filedialog
from functools import partial
from threading import Thread
from tkinter import messagebox, W, N, Label
import requests
from PIL import Image, ImageTk
from io import BytesIO
from ScrollbarFrame import ScrollbarFrame
from consts import *
from mainFrameMethods import invalidateOffersFrame, invalidateNewOffersFrame, createList, initExtraInformationGui, \
    showPhotoViewer


def getArrayOfDictionariesFromCsv(path, dictionaries):
    # Check if the path exists
    if not os.path.exists(path):
        return []
    if "FUTURE" in path:
        with open(path, READ_MODE, newline=NEWLINE, encoding=None, errors='ignore') as file:
            reader = csv.DictReader(file, fieldnames=HEADERS, delimiter=DELIMITER)
            for row in reader:
                dictionaries.append(row)
    else:
        with open(path, READ_MODE, newline=NEWLINE, encoding=ENCODING, errors='ignore') as file:
            reader = csv.DictReader(file, fieldnames=HEADERS, delimiter=DELIMITER)
            for row in reader:
                dictionaries.append(row)

    return dictionaries


def getListEstates(updateOfferLabel, updateNewOfferLabel):
    getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV, offersList)
    getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV, filteredOferList)
    updateOfferLabel()
    getListComparedEstates(newOfferList)
    getListComparedEstates(newFilteredOfferList)
    updateNewOfferLabel()


# Diff from oldGlobalEstates and newGlobalEstates
def getListComparedEstates(distinctEstates):
    oldEstates = []
    getArrayOfDictionariesFromCsv(OLD_ESTATES_CSV, oldEstates)

    if not os.path.isfile(OLD_ESTATES_CSV):
        getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV, newOfferList)
        return None
    newEstates = []
    getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV, newEstates)
    for newEstate in newEstates:
        if not list(filter(lambda estate: estate['nr_oferty'] == newEstate['nr_oferty'], oldEstates)):
            distinctEstates.append(newEstate)

    return None


def filterEstates(filtersDict, mainArray, filteredArray):
    if filtersDict is not None:
        for offer in mainArray:
            shouldAppend = True
            for filterKey in filtersDict:
                if filterKeyDict['type'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['typ'].lower():
                        shouldAppend = False
                if filterKeyDict['priceMin'] == filterKey:
                    if float(filtersDict[filterKey]) >= float(
                            offer['cena'].replace('zł', '').replace(' ', '').replace(',', '.')):
                        shouldAppend = False
                if filterKeyDict['priceMax'] == filterKey:
                    if filtersDict[filterKey] != '':
                        if float(filtersDict[filterKey]) <= float(
                                offer['cena'].replace('zł', '').replace(' ', '').replace(',', '.')):
                            shouldAppend = False
                if filterKeyDict['localization'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['lokalizacja'].lower():
                        shouldAppend = False
                if filterKeyDict['market'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['rynek'].lower():
                        shouldAppend = False
                if filterKeyDict['office'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['nazwa_biura'].replace(' ', '').lower() and \
                            filtersDict[filterKey] != 'WSZYSTKIE':
                        shouldAppend = False
            if shouldAppend:
                filteredArray.append(offer)


# ------------------------------------------------------------------------ #

def createGlobalEstatesCsv():
    # Get newest scrapped data from offices
    listAmerican = getNewestData(AMERICAN_DATA_DIRECTORY)
    listFuture = getNewestData(FUTURE_DATA_DIRECTORY)
    listInvestor = getNewestData(INVESTOR_DATA_DIRECTORY)
    listLandowscy = getNewestData(LANDOWSCY_DATA_DIRECTORY)
    listLevel = getNewestData(LEVEL_DATA_DIRECTORY)

    # Create distinct dictionary with estates
    newGlobalEstates = listAmerican
    dictContenders = listFuture + listInvestor + listLandowscy + listLevel

    # todo distinct na dictionary w trakcie generacji newGlobalEstates lub nie zobaczymy z czasem xD

    newGlobalEstates = newGlobalEstates + dictContenders

    checkForOldGlobalEstates()

    generateCsvFile(newGlobalEstates)


def getNewestData(path):
    array = []
    files = getNewestFile(path)
    if not files:
        # No data from scrapper
        return []

    file = sorted(files, key=os.path.getmtime, reverse=True)[0]

    return getArrayOfDictionariesFromCsv(file, array)


def getNewestFile(path):
    if not os.path.exists(path):
        os.mkdir(path)

    files = os.listdir(path)
    return [os.path.join(path, basename) for basename in files]


def generateCsvFile(list):
    with open(NEW_ESTATES_CSV, WRITING_MODE, newline=NEWLINE, encoding=ENCODING) as csvFile:
        writer = csv.DictWriter(csvFile, delimiter=DELIMITER, fieldnames=HEADERS)
        writer.writerows(list)


def checkForOldGlobalEstates():
    if os.path.isfile(NEW_ESTATES_CSV):
        if os.path.isfile(OLD_ESTATES_CSV):
            os.remove(OLD_ESTATES_CSV)
        os.rename(NEW_ESTATES_CSV, OLD_ESTATES_CSV)


def updateOffers(root, loader, updateOfferLabel, updateNewOffers):
    createGlobalEstatesCsv()
    offersList.clear()
    filteredOferList.clear()
    newOfferList.clear()
    newFilteredOfferList.clear()
    getListEstates(updateOfferLabel, updateNewOffers)
    loader.startLoading()
    invalidateOffersFrame(root, loader)
    invalidateNewOffersFrame(root, loader)

def createMergeWindow(root):
    newWindow = tkinter.Toplevel(root)
    newWindow.withdraw()
    newFrame = tkinter.Frame(newWindow)

    files = tkinter.filedialog.askopenfilenames(parent=newFrame, title='Wybierz pliki')
    msgbox = tkinter.messagebox.askquestion('Dodaj pliki', 'Czy chcesz dodać kolejne pliki?', icon='warning')
    return list(files), msgbox, newWindow

def mergeUniqueValues(files):
    mergedEstates = []
    scanned_data = []
    with open(files[0], READ_MODE, newline=NEWLINE, encoding=ENCODING, errors='ignore') as f:
        reader = csv.DictReader(f, fieldnames=HEADERS, delimiter=DELIMITER)
        for row in reader:
            scanned_data.append(row['data_skanowania'])
            row.pop('data_skanowania')
            mergedEstates.append(row)
    files.pop(0)
    for file in files:
        with open(file, READ_MODE, newline=NEWLINE, encoding=ENCODING, errors='ignore') as f:
            reader = csv.DictReader(f, fieldnames=HEADERS, delimiter=DELIMITER)
            for row in reader:
                scanned_data.append(row['data_skanowania'])
                row.pop('data_skanowania')
                if row not in mergedEstates:
                    mergedEstates.append(row)
    for i in range(len(mergedEstates)):
        mergedEstates[i]['data_skanowania'] = scanned_data[i]
    return mergedEstates

def createTable(mergedEstates, root):
    newWindow = tkinter.Toplevel(root)
    sFrame = ScrollbarFrame(newWindow, 800)
    frame = sFrame.scrolled_frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=3)
    Label(frame, text='typ').grid(column=2, row=0, sticky=N)
    Label(frame, text='cena').grid(column=3, row=0, sticky=N)
    Label(frame, text='lokalizacja').grid(column=4, row=0, sticky=N)
    Label(frame, text='rynek').grid(column=5, row=0, sticky=N)
    Label(frame, text='nazwa_biura').grid(column=6, row=0, sticky=N)
    Thread(target=lambda: populateTable(frame, mergedEstates)).start()
    sFrame.grid(column=0, row=3, sticky=W, padx=5, pady=5)

def populateTable(frame,mergedFile):
    for id, estate in enumerate(mergedFile):
        response = requests.get(estate.get('zdjecie_glowne'))
        try:
            imgLoad = Image.open(BytesIO(response.content))
            imgLoad.thumbnail((58, 58), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(imgLoad)
            photo = tkinter.Label(frame, image=render)
            photo.image = render
            photo.grid(column=0, row=id+1, columnspan=2, sticky=N)
        except:
            print("Temp img didn't find")

        Label(frame, text=estate.get('typ')).grid(column=2, row=id+1, sticky=N)
        Label(frame, text=estate.get('cena')).grid(column=3, row=id+1, sticky=N)
        Label(frame, text=estate.get('lokalizacja')).grid(column=4, row=id+1, sticky=N)
        Label(frame, text=estate.get('rynek')).grid(column=5, row=id+1, sticky=N)
        Label(frame, text=estate.get('nazwa_biura')).grid(column=6, row=id+1, sticky=N)
        action_with_arg = partial(initExtraInformationGui, estate)
        tkinter.Button(frame, text="Zobacz", width=8, command=action_with_arg).grid(column=7, row=id+1, sticky=N)
        showPhotoViewerPartial = partial(showPhotoViewer, estate)
        if estate.get('zdjecia_linki') != '-1':
            tkinter.Button(frame, text="Zdjęcia", width=6, command=showPhotoViewerPartial).grid(column=8, row=id+1, sticky=N)

