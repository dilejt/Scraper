from threading import Thread
from consts import OFFICE_PROPERTY
from scrapers.future.future import startFuture
from scrapers.american.american import startAmerican
from scrapers.investor.investor import startInvestor
from scrapers.level.level import startLevel
from scrapers.landowscy.landowscy import startLandowscy
from backend import createGlobalEstatesCsv


def generateOnClickHandler(officeName, root):
    if officeName == OFFICE_PROPERTY['landowscy']:
        startLandowscy()
    if officeName == OFFICE_PROPERTY['future']:
        Thread(target=lambda: startFuture(root)).start()
    if officeName == OFFICE_PROPERTY['level']:
        startLevel()
    if officeName == OFFICE_PROPERTY['american']:
        startAmerican()
    if officeName == OFFICE_PROPERTY['investor']:
        startInvestor()
    createGlobalEstatesCsv()


def filterOffers():
    print('filtruje sobie rzeczy')
