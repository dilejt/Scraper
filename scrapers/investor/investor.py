from backend import createGlobalEstatesCsv, updateOffers
from scrapers.investor.methods import synchronizeEstates


def startInvestor(root, loader):
    synchronizeEstates(root)
    updateOffers(root, loader)

