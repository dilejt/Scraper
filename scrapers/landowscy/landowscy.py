from progressBar import ProgressBar
from scrapers.landowscy.methods import searchOffers, processOffers, generateCsvFile
from scrapers.landowscy.variables import offerList, subPageToScrap, urls
from consts import HEADERS


def startLandowscy(root):
    urls.clear()
    offerList.clear()
    searchOffers(subPageToScrap)
    progressBar = ProgressBar(root, len(urls))
    processOffers(progressBar)
    generateCsvFile(offerList, HEADERS)
