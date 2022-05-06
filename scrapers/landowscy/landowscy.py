from scrapers.landowscy.methods import searchOffers, processOffers, generateCsvFile
from scrapers.landowscy.variables import fieldNamesDict, offerList


def startLandowscy():
    searchOffers('/lista-ofert/')
    processOffers()
    fieldNamesList = []
    for field in fieldNamesDict:
        fieldNamesList.append(fieldNamesDict[field])
    generateCsvFile(offerList, fieldNamesList)
