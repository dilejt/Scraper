from consts import OFFICE_PROPERTY, offersList, filteredOferList, newFilteredOfferList, newOfferList
from mainFrameMethods import invalidateOffersFrame, invalidateNewOffersFrame
from threading import Thread
from scrapers.future.future import startFuture
from scrapers.american.american import startAmerican
from scrapers.investor.investor import startInvestor
from scrapers.level.level import startLevel
from scrapers.landowscy.landowscy import startLandowscy
from backend import filterEstates


def generateOnClickHandler(officeName, root, loader, updateOfferLabel, updateNewOffers):
    if officeName == OFFICE_PROPERTY['landowscy']:
        Thread(target=lambda: startLandowscy(root, loader, updateOfferLabel, updateNewOffers)).start()
    if officeName == OFFICE_PROPERTY['future']:
        Thread(target=lambda: startFuture(root, loader, updateOfferLabel, updateNewOffers)).start()
    if officeName == OFFICE_PROPERTY['level']:
        Thread(target=lambda: startLevel(root, loader, updateOfferLabel, updateNewOffers)).start()
    if officeName == OFFICE_PROPERTY['american']:
        Thread(target=lambda: startAmerican(root, loader, updateOfferLabel, updateNewOffers)).start()
    if officeName == OFFICE_PROPERTY['investor']:
        Thread(target=lambda: startInvestor(root, loader, updateOfferLabel, updateNewOffers)).start()


def filterOffers(root, loader, type, priceMin, priceMax, localization, market, office, filterType, updateCounter):
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
    if filterType == 'newOffers':
        newFilteredOfferList.clear()
        filterEstates(inputDict, newOfferList, newFilteredOfferList)
        invalidateNewOffersFrame(root, loader)
    else:
        filteredOferList.clear()
        filterEstates(inputDict, offersList, filteredOferList)
        invalidateOffersFrame(root, loader)
    updateCounter()

