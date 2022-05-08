import re
from bs4 import BeautifulSoup
import urllib.request as urllib2
import scrapers.level.Scrap

fields = {
    "typ"  : -1,
    "cena" : -1,
    "typ_transakcji" : -1,
    "dostepny" : -1,
    "powierzchnia" : -1,
    "powierzchnia_dzialki" : -1,
    "link" : -1,
    "liczba_zdjec" : -1,
    "zdjecia_linki" : -1,
    "zdjecie_glowne" : -1,
    "zdjecie_glowne_link" : -1,
    "opis" : -1,
    "rynek" : -1,
    "liczba_pomieszczen" : -1,
    "pietro" : -1,
    "lokalizacja" : -1,
    "cena_za_m2" : -1,
    "typ_zabudowy" : -1,
    "standard_wykonczenia" : -1,
    "rok_budowy" : -1,
    "balkon" : -1,
    "miejsce_parkingowe" : -1,
    "winda" : -1,
    "stan_wykonczenia" : -1,
    "piwnica" : -1,
    "umeblowane" : -1,
    "liczba_lazienek" : -1,
    "numer_oferty" : -1,
    "lokale_uzytkowe" : -1,
    "oplaty" : -1,
    "nr_oferty" : -1,
    "budynek_pietra" : -1,
    "kaucja" : -1,
    "wystawa_okien" : -1,
    "dojazd" : -1,
    "stan_prawny_dzialki" : -1,
    "telefon" : -1,
    "email" : -1,
    "nazwa_biura" : -1,
    "data_dodania_oferty" : -1,
    "data_skanowania" : -1
}

class LevelRealEstates:
    def initGetLevelEstates(self, progressBar):
        print("start")
        Scrap = scrapers.level.Scrap
        getRealEstates = Scrap.PrepareRealEstates()
        getProp = Scrap.RealEstateProperties()
        url = "https://levelnieruchomosci.pl/nieruchomosci"
        realEstatesList = getRealEstates.getData(url)
        realEstatesWithProperties = getProp.getProperties(realEstatesList, fields, progressBar)

    def getRealEstateNumber(self):
        # url = urllib2.urlopen("https://levelnieruchomosci.pl/nieruchomosci")
        # soup = BeautifulSoup(url, features = "html5lib")
        # estateQuantity = soup.find("div", attrs={'class' : 'pull-right search_prop_calc'})
        # number = estateQuantity.get_text().strip()
        # estateQuantity = int(re.findall(r'\d+', number)[2])
        # print(estateQuantity)
        estateQuantity = 20

        return estateQuantity
