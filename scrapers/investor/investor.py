from backend import createGlobalEstatesCsv
from scrapers.investor.methods import synchronizeEstates


def startInvestor():
    synchronizeEstates()
    createGlobalEstatesCsv()