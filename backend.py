import csv
import os
from consts import NEW_ESTATES_CSV, OLD_ESTATES_CSV, HEADERS

#  You have to specify absolute path the file
def getArrayOfDictionariesFromCsv(path):
    # Check if the path exists
    if not os.path.exists(path):
        return []

    dictionaries = []
    with open(path, 'r', newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, fieldnames=HEADERS, delimiter=';')
        for row in reader:
            dictionaries.append(row)

    return dictionaries

def getListEstates(filtersArray = None):
    estates = getArrayOfDictionariesFromCsv(NEW_ESTATES_CSV)

    return filterEstates(estates, filtersArray)

# Diff from oldGlobalEstates and newGlobalEstates
def getListComparedEstates(filtersArray = None):
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