import csv
from datetime import datetime

from consts import *

#  You have to specify absolute path the file
def getArrayOfDictionariesFromCsv(path):
    # Check if the path exists
    if not os.path.exists(path):
        return []

    dictionaries = []
    with open(path, READ_MODE, newline=NEWLINE, encoding=ENCODING) as file:
        reader = csv.DictReader(file, fieldnames=HEADERS, delimiter=DELIMITER)
        for row in reader:
            dictionaries.append(row)

    return dictionaries

def getListEstates(filtersArray=None):
    estates = getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV)

    return filterEstates(estates, filtersArray)

# Diff from oldGlobalEstates and newGlobalEstates
def getListComparedEstates(filtersArray=None):
    newEstates = getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV)
    oldEstates = getArrayOfDictionariesFromCsv(OLD_ESTATES_CSV)

    # todo zrobic distinct pomiedzy estates
    distinctEstates = newEstates

    return filterEstates(distinctEstates, filtersArray)

def filterEstates(estates, filtersArray):
    # todo obsluga filtrów
    if filtersArray is not None:
        return estates
    else:
        return estates

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

    # for contenderEstate in dictContenders: todo dodac jakiegos distincta
    #     for estate in newGlobalEstates:
    #         if compareEstates(estate, contenderEstate):
    #             newGlobalEstates.append(contenderEstate)

    # Write newGlobalEstates to Csv

    # Sprawdz czy istnieje newGlobalEstates, jesli tak to go bziknij na starego
    # dodaj nowa csv
def getNewestData(path):
    files = getNewestFile(path)
    if not files:
        # No data from scrapper
        return []

    file = sorted(files, key=os.path.getmtime, reverse=True)[0]

    return getArrayOfDictionariesFromCsv(file)

def getNewestFile(path):
    if not os.path.exists(path):
        os.mkdir(path)

    files = os.listdir(path)
    return [os.path.join(path, basename) for basename in files]