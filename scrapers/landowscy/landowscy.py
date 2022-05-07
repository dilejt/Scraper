from scrapers.landowscy.methods import searchOffers, processOffers, generateCsvFile
from scrapers.landowscy.variables import offerList, subPageToScrap, urls
from consts import HEADERS


def startLandowscy():
    print('Zapisuje oferty do tablicy')
    searchOffers(subPageToScrap)
    print('Mam do sprawdzenia: ' + str(len(urls)) + ' ofert')
    print('Pobieram szczegoly ofert')
    processOffers()
    print('Zapisuje do pliku znalezione oferty')
    generateCsvFile(offerList, HEADERS)
    print('Koniec scrapowania biura: landowscy nieruchomosci')
