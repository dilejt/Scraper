from tkinter import W
from tkinter.filedialog import askopenfilename

from consts import DELIMITER, ENCODING, NEWLINE, OFFICE_PROPERTY, ROOT_DIR, WRITING_MODE, offersList, NEW_ESTATES_CSV, filteredOferList
from mainFrameMethods import createList, invalidateOffersFrame
from threading import Thread
from mergedCsvFrame import mergedCsvFrame
from scrapers.future.future import startFuture
from scrapers.american.american import startAmerican
from scrapers.investor.investor import startInvestor
from scrapers.level.level import startLevel
from scrapers.landowscy.landowscy import startLandowscy
from backend import filterEstates, createGlobalEstatesCsv, getArrayOfDictionariesFromCsv
import pandas as pd


def generateOnClickHandler(officeName, root, loader):
    if officeName == OFFICE_PROPERTY['landowscy']:
        Thread(target=lambda: startLandowscy(root, loader)).start()
    if officeName == OFFICE_PROPERTY['future']:
        Thread(target=lambda: startFuture(root, loader)).start()
    if officeName == OFFICE_PROPERTY['level']:
        startLevel(root, loader)
    if officeName == OFFICE_PROPERTY['american']:
        Thread(target=lambda: startAmerican(root, loader)).start()
    if officeName == OFFICE_PROPERTY['investor']:
        Thread(target=lambda: startInvestor(root, loader)).start()


def filterOffers(container, loader, type, priceMin, priceMax, localization, market, office):
    loader.startLoading()
    if priceMin == '':
        priceMin = 0
    inputDict = {
        'type': type,
        'priceMin': priceMin,
        'priceMax': priceMax,
        'localization': localization,
        'market': market,
        'office': office,
    }
    filterEstates(inputDict)
    invalidateOffersFrame(container, loader)

def mergeChosenCsvOnClickHandler():
    firstCsvFilename = askopenfilename()
    secondCsvFilename = askopenfilename()
    mergedCsvFrameClass = mergedCsvFrame()

    if (firstCsvFilename.endswith("csv") and secondCsvFilename.endswith("csv")):
        firstCsvFile = pd.read_csv(firstCsvFilename, header=None, engine='python', encoding=ENCODING, sep=DELIMITER)
        secondCsvFile = pd.read_csv(secondCsvFilename, header=None, engine='python', encoding=ENCODING, sep=DELIMITER)

        combined_csv = pd.concat([firstCsvFile, secondCsvFile])
        combined_csv.to_csv( "combined_csv.csv", sep=DELIMITER, index=False, header=False)

        mergedCsvFrameClass.showMergedCsvFiles()
    else:
        print("Wrong file/files was/were chosen. Choose .csv files to merge.")


