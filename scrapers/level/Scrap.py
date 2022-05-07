import re
import urllib.request as urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime

from numpy import double
from consts import DELIMITER, ENCODING, NEWLINE, OFFICE_PROPERTY, WRITING_MODE
from helpers import getFileName


field_names = ["typ", "cena", "typ_transakcji", "dostepny", "powierzchnia", "powierzchnia_dzialki", "link", "liczba_zdjec", "zdjecia_linki", "zdjecie_glowne", "zdjecie_glowne_link", "opis", "rynek", "liczba_pomieszczen", "pietro", "lokalizacja", "cena_za_m2", "typ_zabudowy", "standard_wykonczenia", "rok_budowy", "balkon", "miejsce_parkingowe", "winda", "stan_wykonczenia", "piwnica", "umeblowane", "liczba_lazienek", "numer_oferty", "lokale_uzytkowe", "oplaty", "nr_oferty", "budynek_pietra", "kaucja", "wystawa_okien", "dojazd", "stan_prawny_dzialki", "telefon", "email", "nazwa_biura", "data_dodania_oferty", "data_skanowania"]
appendArray = []
scanDate = datetime.now()

class PrepareRealEstates:
    offers = []

    def getData(self, url):
        self.url =  urllib2.urlopen(url)
        self.soup = BeautifulSoup(self.url, features = "html5lib")
        pages = getPages(self, url)
        realEstateList = getRealEstateList(self, pages)

        return realEstateList

class RealEstateProperties:
    def getProperties(self, realEstatesList, fields):
        self.realEstatesList = realEstatesList
        self.fields = fields
        print("Getting sites properties...")

        for realEstate in self.realEstatesList:
            self.url = urllib2.urlopen(realEstate)
            self.soup = BeautifulSoup(self.url, features = "html5lib")
            textPropertyArray = fetchPropertyText(self, self.soup)
            gallery = ""
            imageCounter = 0

            for i in self.soup.findAll('a', attrs = {'class' : "galleryItem"}):
                gallery += i.get('href') + ","
                imageCounter += 1
            
            fetchedFields = {
                "typ" : textPropertyArray[0],
                "cena" :  textPropertyArray[1],
                "typ_transakcji" :  textPropertyArray[2],
                "powierzchnia" : textPropertyArray[3],
                "powierzchnia_dzialki" :  textPropertyArray[4],
                "link" : realEstate,
                "liczba_zdjec" : imageCounter,
                "zdjecia_linki" :  gallery,
                "zdjecie_glowne" :  textPropertyArray[5],
                "zdjecie_glowne_link" : textPropertyArray[6],
                "opis" :  textPropertyArray[7],
                "lokalizacja" :  textPropertyArray[8],
                "cena_za_m2" :  textPropertyArray[9],
                "liczba_lazienek" :  textPropertyArray[10],
                "liczba_pomieszczen" : textPropertyArray[11],
                "nazwa_biura" : "Level nieruchomości",
                "data_skanowania" : scanDate
            }
            appendArray.append(overwriteFields(self, fetchedFields, fields).copy())

        saveToFile(self, appendArray)

def getPages(self, url):
    pages = []

    for page in self.soup.findAll('a', attrs = {'href': re.compile("page*")}):
        pages.append(page.get('href'))

    firstPage = int("".join(re.findall(r'\d+', pages[1])))
    lastPage = int("".join(re.findall(r'\d+', pages[-1])))
    pages = []

    for page in range(firstPage, lastPage + 1):
        pages.append(url + "/page/" + str(page))

    pages.insert(0, url)

    return pages

def getRealEstateList(self, pages):
    realEstates = []

    for page in pages:
        self.url = urllib2.urlopen(page)
        self.soup = BeautifulSoup(self.url, features = "html5lib")
        realEstates = getRealEstates(self, realEstates)

    return realEstates

def getRealEstates(self, realEstates):
    for realEstate in self.soup.findAll('a', limit = 2,  attrs = {'id': re.compile("card*")}):
        if realEstate not in realEstates:
            realEstates.append(realEstate.get('href'))

    return realEstates

def fetchPropertyText(self, soup):
    i = 0
    bathrooms = -1
    rooms = -1

    try:
        bathrooms = soup.find('span', attrs = {'class' : 'icon-drop'}).findNext('div', string = re.compile("[^0-9]"))
    except:
        print("bathroom not found")

    try:
        rooms = soup.find('span', attrs = {'class' : 'fa fa-moon-o'}).findNext('div', string = re.compile("[^0-9]"))
    except:
        print("room not found")

    arr = [soup.find('div', attrs = {'class' : "listCategory"}),
    soup.find('div', attrs = {'class' : "listPrice"}),
    soup.find('span', attrs = {'class' : "label label-yellow"}),
    soup.find('div', string = re.compile("[0-9,] m²")),
    soup.find('div', string = re.compile("[0-9,] m²")),
    soup.find('a', attrs = {'class' : "galleryItem item active"}),
    soup.find('a', attrs = {'class' : "galleryItem item active"}),
    soup.find('div', attrs = {'class' : "description"}),
    soup.find('div', attrs = {'class' : "address"}),
    soup.find('div', string = re.compile("[0-9,] PLN za m²")),
    bathrooms,
    rooms,
    ]

    for property in arr:
        try:
            propTxt = property.get_text().strip()

            if (i == 3 or i == 4 or i == 9):
                propTxt = double(re.findall(r'\d+', propTxt)[0])

            if (i == 10 or i == 11 ):
                propTxt = int(re.findall(r'\d+', propTxt)[0])
            
            if (i == 1):
                propTxt = int(re.findall(r'\d+', propTxt)[0] + re.findall(r'\d+', propTxt)[1])

        except:
            propTxt = -1

        arr[i] = propTxt

        if i == 5 | i == 6:
            arr[i] = property.get('href')

        i += 1

    return arr

def overwriteFields(self, fetchedFields, fields):
    for key in fields:
        if key in fetchedFields:
            fields[key] = fetchedFields[key]

    return fields

def saveToFile(self, appendArray):
    with open(getFileName(OFFICE_PROPERTY['level']), WRITING_MODE, newline = NEWLINE, encoding = ENCODING) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = field_names, delimiter = DELIMITER)
            writer.writeheader()
            writer.writerows(appendArray)