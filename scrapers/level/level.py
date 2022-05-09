from backend import createGlobalEstatesCsv, updateOffers
from progressBar import ProgressBar
from scrapers.level.Initialize import LevelRealEstates


def startLevel(self, loader):
    levelRealEstates = LevelRealEstates()
    progressBar = ProgressBar(self.root, levelRealEstates.getRealEstateNumber())
    levelRealEstates.initGetLevelEstates(progressBar)
    updateOffers(self, loader)
