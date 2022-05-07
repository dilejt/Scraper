from tkinter import W

from consts import OFFICE_PROPERTY, offersList, NEW_ESTATES_CSV, filteredOferList
from mainFrameMethods import createList, invalidateOffersFrame
from scrapers.future.future import startFuture
from scrapers.american.american import startAmerican
from scrapers.investor.investor import startInvestor
from scrapers.level.level import startLevel
from scrapers.landowscy.landowscy import startLandowscy
from backend import filterEstates, getArrayOfDictionariesFromCsv


def generateOnClickHandler(officeName):
    if officeName == OFFICE_PROPERTY['landowscy']:
        startLandowscy()
    if officeName == OFFICE_PROPERTY['future']:
        startFuture()
    if officeName == OFFICE_PROPERTY['level']:
        startLevel()
    if officeName == OFFICE_PROPERTY['american']:
        startAmerican()
    if officeName == OFFICE_PROPERTY['investor']:
        startInvestor()


def filterOffers(frame, container, type, priceMin, priceMax, localization, market, office):
    if priceMin == '':
        priceMin = 0
    inputDict = {
        'type': type,
        'priceMin': priceMin,
        'priceMax': priceMax,
        'localization': localization,
        'market': market,
        'office': office,
    }
    filterEstates(inputDict)
    invalidateOffersFrame(frame, container)
