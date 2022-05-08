from tkinter import W

from consts import OFFICE_PROPERTY, offersList, NEW_ESTATES_CSV, filteredOferList
from mainFrameMethods import createList, invalidateOffersFrame
from threading import Thread
from scrapers.future.future import startFuture
from scrapers.american.american import startAmerican
from scrapers.investor.investor import startInvestor
from scrapers.level.level import startLevel
from scrapers.landowscy.landowscy import startLandowscy
from backend import filterEstates, createGlobalEstatesCsv, getArrayOfDictionariesFromCsv


def generateOnClickHandler(officeName, root, loader):
    if officeName == OFFICE_PROPERTY['landowscy']:
        Thread(target=lambda: startLandowscy(root, loader)).start()
    if officeName == OFFICE_PROPERTY['future']:
        Thread(target=lambda: startFuture(root)).start()
    if officeName == OFFICE_PROPERTY['level']:
        startLevel()
    if officeName == OFFICE_PROPERTY['american']:
        Thread(target=lambda: startAmerican(root)).start()
    if officeName == OFFICE_PROPERTY['investor']:
        startInvestor()


def filterOffers(container, loader, type, priceMin, priceMax, localization, market, office):
    loader.startLoading()
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
    invalidateOffersFrame(container, loader)

