import csv
import re
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

from consts import OFFICE_PROPERTY, WRITING_MODE, DELIMITER, NEWLINE, ENCODING
from helpers import getFileName
from scrapers.landowscy.variables import *


def searchOffers(url, offset):
    htmlCode = urllib.request.urlopen(urlDomain + url + '/?offset=' + str(offset))
    soup = BeautifulSoup(htmlCode, 'html.parser', from_encoding="utf-8")
    numberOfOffers = soup.select_one(".search-count")
    for item in soup.find_all('a', class_="property-row-image", href=True):
        urls.append(item['href'])
    # if offset < int(numberOfOffers.text) - 20:
    #     offset += 20
    #     searchOffers(url,offset)
    if offset < 20:
        offset += 20
        searchOffers(url, offset)
    # if offset < 0:
    #     offset += 20
    #     searchOffers(url, offset)


def processOffers(progressBar):
    for url in urls:
        progressBar.progress()
        checkOffer(url)


def checkOffer(url):
    htmlCode = urllib.request.urlopen(urlDomain + url)
    soup = BeautifulSoup(htmlCode, 'html.parser', from_encoding="utf-8")
    keyArray = []
    valueArray = []
    for item in soup.find_all('dt'):
        keyArray.append(item.text)
    for item in soup.find_all('dd'):
        if item.text == 'Tak':
            valueArray.append(True)
        elif item.text == 'Parter':
            valueArray.append(0)
        else:
            valueArray.append(item.text)
    dictionaryTable = dict(zip(keyArray, valueArray))
    urlDivided = url.split("-")
    localization = ''
    for index in range(4, len(urlDivided) - 1):
        localization += ' ' + urlDivided[index]
    description = re.sub(' +', ' ', soup.find("p", class_="text").text)
    email = soup.find("li", class_="email").text
    phoneNumber = re.findall(r"\d{3}\s\d{3}\s\d{3}", description)
    if len(phoneNumber) == 0:
        phoneNumber.append('667 376 116')
    mainPhotoUrl = soup.find('div', class_='property-gallery-preview').a.img.get('src')
    photosUrl = []
    for item in soup.find_all('div', class_="property-gallery-list-item active"):
        photosUrl.append(urlDomain + item.a.img.get('src'))
    offer = {
        'link': urlDomain + url,
        'typ': urlDivided[0].replace('/', ''),
        'typ_transakcji': urlDivided[1],
        'lokalizacja': localization,
        'telefon': phoneNumber[0],
        'email': email,
        'nazwa_biura': 'LANDOWSCY NIERUCHOMOŚCI',
        'data_skanowania': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'zdjecie_glowne_link': urlDomain + mainPhotoUrl,
        'zdjecie_glowne': urlDomain + mainPhotoUrl,
        'zdjecia_linki': photosUrl,
        'liczba_zdjec': len(photosUrl),
        'opis': description,
    }
    for key in dictionaryTable:
        if key in fieldNamesDict.keys():
            value = dictionaryTable[key]
            if key == 'Cena':
                value = dictionaryTable[key].replace('PLN', '').replace(' ', '')
            if key == 'Cena za m2' or key == 'Czynsz administracyjny':
                value = dictionaryTable[key].replace('PLN', '').replace(' ', '').replace(',', '.')
            if key == 'Powierzchnia' or key == 'Powierzchnia działki':
                value = dictionaryTable[key].replace('m2', '').replace(' ', '').replace(',', '.').replace('\xa0', '')
            offer[fieldNamesDict[key]] = value
    if 'balkon' in description:
        offer['balkon'] = True
    if 'piwnica' in description:
        offer['piwnica'] = True
    if 'meblowan' in description:
        offer['umeblowane'] = True
    for item in soup.find_all('li', class_="yes"):
        if 'Winda' in item:
            offer['winda'] = True
    for key in fieldNamesDict:
        if fieldNamesDict[key] not in offer.keys():
            offer[fieldNamesDict[key]] = -1
    offerList.append(offer)


def generateCsvFile(list, fieldNames):
    with open(getFileName(OFFICE_PROPERTY['landowscy']), WRITING_MODE, newline=NEWLINE, encoding=ENCODING) as csvFile:
        writer = csv.DictWriter(csvFile, delimiter=DELIMITER, fieldnames=fieldNames)
        writer.writerows(list)
