from backend import updateOffers
from scrapers.investor.methods import synchronizeEstates


def startInvestor(self, loader):
    synchronizeEstates(self.root)
    updateOffers(self, loader)

