from backend import updateOffers
from scrapers.investor.methods import synchronizeEstates


def startInvestor(root, loader, updateOfferLabel, updateNewOffers):
    synchronizeEstates(root)
    updateOffers(root, loader, updateOfferLabel, updateNewOffers)

