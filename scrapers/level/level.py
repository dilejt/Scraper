from backend import createGlobalEstatesCsv, updateOffers
from progressBar import ProgressBar
from scrapers.level.Initialize import LevelRealEstates


def startLevel(root, loader):
    levelRealEstates = LevelRealEstates()
    progressBar = ProgressBar(root, levelRealEstates.getRealEstateNumber())
    levelRealEstates.initGetLevelEstates(progressBar)
    updateOffers(root, loader)
