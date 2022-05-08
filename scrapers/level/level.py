from backend import createGlobalEstatesCsv, updateOffers
from scrapers.level.Initialize import LevelRealEstates


def startLevel(root, loader):
    LevelRealEstates.initGetLevelEstates()
    updateOffers(root, loader)
