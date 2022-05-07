import csv
import os
from consts import NEW_ESTATES_CSV, OLD_ESTATES_CSV, HEADERS, READ_MODE, NEWLINE, ENCODING, DELIMITER, offersList, \
    filterKeyDict, filteredOferList


#  You have to specify absolute path the file
def getArrayOfDictionariesFromCsv(path, dictionaries):
    # Check if the path exists
    if not os.path.exists(path):
        return []

    with open(path, READ_MODE, newline=NEWLINE, encoding=ENCODING) as file:
        reader = csv.DictReader(file, fieldnames=HEADERS, delimiter=DELIMITER)
        for row in reader:
            dictionaries.append(row)

    return dictionaries


def getListEstates():
    getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV, offersList)
    getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV, filteredOferList)
    filterEstates(None)


# Diff from oldGlobalEstates and newGlobalEstates
def getListComparedEstates(filtersArray=None):
    newEstates = getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV)
    oldEstates = getArrayOfDictionariesFromCsv(OLD_ESTATES_CSV)

    # todo zrobic distinct pomiedzy estates
    distinctEstates = newEstates

    return filterEstates(distinctEstates, filtersArray)


def filterEstates(filtersDict):
    if filtersDict is not None:
        filteredOferList.clear()
        for offer in offersList:
            shouldAppend = True
            for filterKey in filtersDict:
                if filterKeyDict['type'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['typ'].lower():
                        shouldAppend = False
                if filterKeyDict['priceMin'] == filterKey:
                    if int(filtersDict[filterKey]) >= int(offer['cena'].replace('zł', '').replace(' ', '')):
                        shouldAppend = False
                if filterKeyDict['priceMax'] == filterKey:
                    if filtersDict[filterKey] != '':
                        if int(filtersDict[filterKey]) <= int(offer['cena'].replace('zł', '').replace(' ', '')):
                            shouldAppend = False
                if filterKeyDict['market'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['rynek'].lower():
                        shouldAppend = False
                if filterKeyDict['office'] == filterKey:
                    if filtersDict[filterKey].lower() not in offer['nazwa_biura'].replace(' ', '').lower() and filtersDict[filterKey] != 'WSZYSTKIE':
                        shouldAppend = False
            if shouldAppend:
                filteredOferList.append(offer)

