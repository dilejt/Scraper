from backend import createGlobalEstatesCsv
from scrapers.level.Initialize import LevelRealEstates


def startLevel():
    LevelRealEstates.initGetLevelEstates()
    createGlobalEstatesCsv()