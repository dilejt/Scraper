from backend import updateOffers
from progressBar import ProgressBar
from scrapers.landowscy.methods import searchOffers, processOffers, generateCsvFile
from scrapers.landowscy.variables import offerList, subPageToScrap, urls
from consts import HEADERS


def startLandowscy(self, loader):
    urls.clear()
    offerList.clear()
    offset = 0
    searchOffers(subPageToScrap, offset)
    progressBar = ProgressBar(self.root, len(urls))
    processOffers(progressBar)
    generateCsvFile(offerList, HEADERS)
    updateOffers(self, loader)
