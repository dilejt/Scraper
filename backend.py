import csv
from consts import *
from mainFrameMethods import invalidateOffersFrame, invalidateNewOffersFrame


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
