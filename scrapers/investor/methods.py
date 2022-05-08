import urllib
import urllib.parse
import urllib.request
from datetime import datetime

from progressBar import ProgressBar
from scrapers.investor.RowStructure import RowStructure
from bs4 import BeautifulSoup
from pathlib import Path
import csv

def getUrlContent(url):
    request = urllib.request.urlopen(url)
    return request.read().decode(request.headers.get_content_charset())

def processUrlContent(soup, host):
    tempLinksArray = []
    for url in soup.find_all(id="cnv-offer-details"):
        tempLinksArray.append(urllib.parse.urljoin(host, url.get('href')))
    return tempLinksArray

def getMaxOffsetPagination(soup):
    paginationArray = []
    for url in soup.find_all("a", {"class": "real-btn"}):
        if url.string.isdigit():
            paginationArray.append(int(url.string))
    return max(paginationArray)

def getPage(page, host):
    homeUrl = 'https://investor.net.pl/nieruchomosci/?offset=' + str(page)
    urlContent = getUrlContent(homeUrl)
    soup = BeautifulSoup(urlContent, 'html.parser')
    return processUrlContent(soup, host)

def synchronizeEstates(root):
    homeUrl = "https://investor.net.pl/nieruchomosci/"
    host = "https://investor.net.pl/"

    urlContent = getUrlContent(homeUrl)
    soup = BeautifulSoup(urlContent, 'html.parser')
    arrayUrls = processUrlContent(soup, host)
    dictionaryArray = []
    maxOffsetPagination = getMaxOffsetPagination(soup)
    progressBar = ProgressBar(root, 10)

    for url in arrayUrls:
        dataRow = processLinkEstate(url, host)
        if dataRow is not None:
            dictionaryArray.append(dataRow)
    # Get data from other pages
    dictionaryArray = dictionaryArray + getEstateInfoPagination(maxOffsetPagination, host, progressBar)
    # save dictionaryArray
    saveToCsv(dictionaryArray)

def saveToCsv(dictionaryArray):
    directory = Path.cwd() / "data" / "investor"

    if not directory.exists():
        directory.mkdir(parents=False, exist_ok=False)
    # Save new data
    fileName = 'INVESTOR_'+str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + '.csv'
    with open(directory / fileName, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(dictionaryArray)

def getEstateInfoPagination(maxOffsetPagination, host, progressBar):
    dictionaryArrayNestedPages = []
    for page in range(10, 20, 10):
        for url in getPage(page, host):
            progressBar.progress()
            dataRow = processLinkEstate(url, host)
            if dataRow is not None:
                dictionaryArrayNestedPages.append(dataRow)
    return dictionaryArrayNestedPages

def processLinkEstate(url, host):
    urlContent = getUrlContent(url)
    print(url)
    soup = BeautifulSoup(urlContent, 'html.parser')
    dictionaryEstate = {}
    # Get data from site - main fields
    try:
        mainFields = soup.find(id="property-main-fields")
        mainFieldsTopics = mainFields.find_all("dt")
        mainFieldsValues = mainFields.find_all("dd")
        for id, value in enumerate(mainFieldsValues):
            dictionaryEstate[mainFieldsTopics[id].text] = value.text
    except AttributeError:
        print("Checked Estate doesn't have main fields")
        return

    # Get data from site - secondary fields
    try:
        secondaryFields = soup.find(id="property-extra-fields")
        secondaryFieldsTopics = secondaryFields.find_all("dt")
        secondaryFieldsValues = secondaryFields.find_all("dd")

        for id, value in enumerate(secondaryFieldsValues):
            dictionaryEstate[secondaryFieldsTopics[id].text] = value.text
    except AttributeError:
        print("Checked Estate doesn't have additional fields")

    # Get type of estate
    header = soup.find("header", {"class": "property-title row"})
    estateType = header.find("p", {"class": "type"})

    # Get photo
    photoUrlRelative = soup.find("a", {"data-idx": 0}).find("img").get("src")
    photoUrl = urllib.parse.urljoin(host, photoUrlRelative)

    # Get description
    try:
        description = soup.find("div", {"class": "text"}).text
        description.strip()
    except AttributeError:
        description = ""

    # Get location
    title = soup.find("header", {"class": "property-title row"})
    city = title.find("h1").text
    try:
        street = title.find("h2").text
        location = city + ", " + street
    except AttributeError:
        location = city

    # Get telephone
    telephone = soup.find(id="cnv-agent-phone").text

    recordToCsv = []
    if estateType.text == 'Mieszkanie na sprzedaż' or estateType.text == 'Mieszkanie na wynajem':
        recordToCsv = processApartment(dictionaryEstate, url, photoUrl, description, location, telephone,
                                       estateType.text)
    elif estateType.text == 'Dom na sprzedaż' or estateType.text == 'Dom na wynajem':
        recordToCsv = processHouse(dictionaryEstate, url, photoUrl, description, location, telephone, estateType.text)
    elif estateType.text == 'Działka na sprzedaż' or estateType.text == 'Działka na wynajem':
        recordToCsv = processPlot(dictionaryEstate, url, photoUrl, description, location, telephone, estateType.text)
    elif estateType.text == 'Lokal na sprzedaż' or estateType.text == 'Lokal na wynajem':
        recordToCsv = processPlace(dictionaryEstate, url, photoUrl, description, location, telephone, estateType.text)
    elif estateType.text == 'Obiekt na sprzedaż' or estateType.text == 'Obiekt na wynajem':
        recordToCsv = processObject(dictionaryEstate, url, photoUrl, description, location, telephone, estateType.text)
    else:
        return
    return recordToCsv

def processApartment(dictionaryEstate, url, photoUrl, description, location, telephone, estateType):
    row = RowStructure()
    row.set_typ(estateType)
    row.set_cena(dictionaryEstate.get('Cena', -1))
    row.set_powierzchnia(dictionaryEstate.get('Powierzchnia', -1))
    row.set_link(url)
    row.set_zdjecie_glowne(photoUrl)
    row.set_opis(description)
    row.set_rynek(dictionaryEstate.get('Rynek', -1))
    row.set_liczba_pomieszczen(dictionaryEstate.get('liczba pokoi', -1))
    row.set_pietro(dictionaryEstate.get('Piętro', -1))
    row.set_lokalizacja(location)
    row.set_cena_za_m2(dictionaryEstate.get('Cena za m2', -1))
    row.set_stan_wykonczenia(dictionaryEstate.get('Stan nieruchomości', -1))
    row.set_rok_budowy(dictionaryEstate.get('Rok budowy', -1))
    row.set_miejsce_parkingowe(dictionaryEstate.get('Garaż/Miejsca parkingowe', -1))
    row.set_winda(dictionaryEstate.get('Winda', -1))
    row.set_oplaty(dictionaryEstate.get('Czynsz administracyjny', -1))
    row.set_nr_oferty(dictionaryEstate.get('Numer oferty', -1))
    row.set_budynek_pietra(dictionaryEstate.get('Liczba pięter', -1))
    row.set_telefon(telephone)
    row.set_data_skanowania(datetime.now())
    row.set_nazwa_biura('investor')

    return row.toArray()

def processHouse(dictionaryEstate, url, photoUrl, description, location, telephone, estateType):
    row = RowStructure()
    row.set_link(url)
    row.set_zdjecie_glowne(photoUrl)
    row.set_opis(description)
    row.set_lokalizacja(location)
    row.set_telefon(telephone)
    row.set_typ(estateType)
    row.set_nr_oferty(dictionaryEstate.get('Numer oferty', -1))
    row.set_cena(dictionaryEstate.get('Cena', -1))
    row.set_powierzchnia(dictionaryEstate.get('Powierzchnia', -1))
    row.set_powierzchnia_dzialki(dictionaryEstate.get('Powierzchnia działki', -1))
    row.set_liczba_pomieszczen(dictionaryEstate.get('Liczba pomieszczeń', -1))
    row.set_budynek_pietra(dictionaryEstate.get('Liczba pięter', -1))
    row.set_stan_wykonczenia(dictionaryEstate.get('Stan nieruchomości', -1))
    row.set_rok_budowy(dictionaryEstate.get('Rok budowy', -1))
    row.set_rynek(dictionaryEstate.get('Rynek', -1))
    row.set_miejsce_parkingowe(dictionaryEstate.get('Garaż/Miejsca parkingowe', -1))
    row.set_dojazd(dictionaryEstate.get('Droga dojazdowa:', -1))
    row.set_data_skanowania(datetime.now())
    row.set_nazwa_biura('investor')

    return row.toArray()

def processPlot(dictionaryEstate, url, photoUrl, description, location, telephone, estateType):
    row = RowStructure()
    row.set_link(url)
    row.set_zdjecie_glowne(photoUrl)
    row.set_opis(description)
    row.set_lokalizacja(location)
    row.set_telefon(telephone)
    row.set_typ(estateType)
    row.set_nr_oferty(dictionaryEstate.get('Numer oferty', -1))
    row.set_cena(dictionaryEstate.get('Cena', -1))
    row.set_cena_za_m2(dictionaryEstate.get('Cena za m2', -1))
    row.set_powierzchnia_dzialki(dictionaryEstate.get('Powierzchnia działki', -1))
    row.set_data_skanowania(datetime.now())
    row.set_nazwa_biura('investor')

    return row.toArray()

def processPlace(dictionaryEstate, url, photoUrl, description, location, telephone, estateType):
    row = RowStructure()
    row.set_link(url)
    row.set_zdjecie_glowne(photoUrl)
    row.set_opis(description)
    row.set_lokalizacja(location)
    row.set_telefon(telephone)
    row.set_typ(estateType)
    row.set_nr_oferty(dictionaryEstate.get('Numer oferty', -1))
    row.set_cena(dictionaryEstate.get('Cena', -1))
    row.set_cena_za_m2(dictionaryEstate.get('Cena za m2', -1))
    row.set_powierzchnia(dictionaryEstate.get('Powierzchnia', -1))
    row.set_pietro(dictionaryEstate.get('Piętro', -1))
    row.set_stan_wykonczenia(dictionaryEstate.get('Stan nieruchomości', -1))
    row.set_rynek(dictionaryEstate.get('Rynek', -1))
    row.set_data_skanowania(datetime.now())
    row.set_nazwa_biura('investor')

    return row.toArray()

def processObject(dictionaryEstate, url, photoUrl, description, location, telephone, estateType):
    row = RowStructure()
    row.set_link(url)
    row.set_zdjecie_glowne(photoUrl)
    row.set_opis(description)
    row.set_lokalizacja(location)
    row.set_telefon(telephone)
    row.set_typ(estateType)
    row.set_nr_oferty(dictionaryEstate.get('Numer oferty', -1))
    row.set_cena(dictionaryEstate.get('Cena', -1))
    row.set_cena_za_m2(dictionaryEstate.get('Cena za m2', -1))
    row.set_powierzchnia(dictionaryEstate.get('Powierzchnia', -1))
    row.set_powierzchnia_dzialki(dictionaryEstate.get('Powierzchnia działki', -1))
    row.set_rok_budowy(dictionaryEstate.get('Rok budowy', -1))
    row.set_rynek(dictionaryEstate.get('Rynek', -1))
    row.set_budynek_pietra(dictionaryEstate.get('Liczba pięter', -1))
    row.set_dojazd(dictionaryEstate.get('Droga dojazdowa:', -1))
    row.set_data_skanowania(datetime.now())
    row.set_nazwa_biura('investor')

    return row.toArray()







