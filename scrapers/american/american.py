import sys
import urllib.request
from bs4 import BeautifulSoup
from datetime import date
import re
import csv

from backend import createGlobalEstatesCsv
from consts import OFFICE_PROPERTY, NEWLINE, WRITING_MODE, DELIMITER, ENCODING, HEADERS
from progressBar import ProgressBar
from scrapers.american.myhelpers import TEMP_ARR, TEMPLATE, LINKS, FIELD_NAMES, APARTMENT, PLOT, HOUSE, TYPES
from helpers import getFileName


class Searcher:
    progressBar = None
    today = date.today()
    result = []
    offers_len = 0
    offers = {
        'mieszkanie': {
            'count': 1,
            'links': []
        },
        'dom': {
            'count': 1,
            'links': []
        },
        'dzialka': {
            'count': 1,
            'links': []
        },
        'lokal': {
            'count': 2,
            'links': []
        },
    }

    def get_value(self, value):
        value = dict(zip(range(len(value)), value))
        if value.get(1):
            temp_text = str(value.get(1))
            temp_text = temp_text.replace('<sup>', '')
            temp_text = temp_text.replace('</sup>', '')
            return str(value.get(0)) + temp_text
        else:
            return str(value.get(0))

    def find_values(self, offer, key, temp_arr):
        temp = temp_arr.copy()
        r = urllib.request.urlopen(offer)
        soup = BeautifulSoup(r, "html.parser")
        photos = ''
        count_photos = 0
        temp['typ'] = key
        temp['link'] = offer
        temp['nazwa_biura'] = 'American Home'
        for values in soup.findAll('div', class_='area'):
            if values.strong.previous_sibling.find('<sup>'):
                if 'Piętro' == values.strong.previous_sibling.get_text():
                    if re.findall("(.*)/.", self.get_value(values.strong.contents)):
                        temp['pietro'] = re.findall("(.*)/.", self.get_value(values.strong.contents))[0]
                    if re.findall(".*/(.*)", self.get_value(values.strong.contents)):
                        temp['budynek_pietra'] = re.findall(".*/(.*)", self.get_value(values.strong.contents))[0]
                elif 'dzialka' == key and 'Powierzchnia' == values.strong.previous_sibling.get_text():
                    temp['powierzchnia_dzialki'] = self.get_value(values.strong.contents)
                elif 'Cena' == values.strong.previous_sibling.get_text():
                    temp['cena'] = ''.join(re.findall("(\d*\d)", self.get_value(values.strong.contents)))
                elif 'Numer oferty' == values.strong.previous_sibling.get_text():
                    temp['numer_oferty'] = self.get_value(values.strong.contents)
                    temp['nr_oferty'] = self.get_value(values.strong.contents)
                elif values.strong.previous_sibling.get_text() in FIELD_NAMES:
                    temp[FIELD_NAMES[values.strong.previous_sibling.get_text()]] = self.get_value(
                        values.strong.contents)
            else:
                if values.strong.previous_sibling.previous_sibling + values.strong.previous_sibling.get_text() in FIELD_NAMES:
                    temp[FIELD_NAMES[
                            values.strong.previous_sibling.previous_sibling + values.strong.previous_sibling.get_text()]] = self.get_value(
                        values.strong.contents)

        for values in soup.findAll('div', class_='tab-pane fade active in'):
            temp['opis'] = values.find_next(class_='property-detail_overview').get_text()
        for values in soup.findAll('i', class_='fa fa-phone'):
            temp['telefon'] = values.find_next('a').get_text()
        for values in soup.findAll('i', class_='fa fa-envelope-o'):
            temp['email'] = values.find_next('a').get_text()
        for values in soup.findAll('a', class_='blueimp'):
            photos += "https://www.americanhome.pl/" + values['href'] + ','
            count_photos = count_photos + 1
        temp['zdjecia_linki'] = photos
        temp['zdjecie_glowne'] = photos.split(',')[0]
        temp['zdjecie_glowne_link'] = photos.split(',')[0]
        temp['liczba_zdjec'] = count_photos
        temp['data_skanowania'] = self.today.strftime("%d/%m/%Y")
        print(temp)
        self.progressBar.progress()
        return temp

    def countpages(self):
        for link in LINKS:
            r = urllib.request.urlopen(link)
            soup = BeautifulSoup(r, "html.parser", from_encoding="iso-8859-1")
            for offer in soup.findAll('ul', class_='pagination pull-right'):
                pages = offer.findAll('li')
                self.offers[TYPES[(link.split('/'))[4]]]['count'] = len(pages)

    def searchoffers(self):
        for link in LINKS:
            for i in range(1, self.offers[TYPES[(link.split('/'))[4]]]['count']):
                if len(self.offers[TYPES[(link.split('/'))[4]]]['links']) >= 5:
                    continue
                r = urllib.request.urlopen(link + '?page=' + str(i))
                soup = BeautifulSoup(r, "html.parser", from_encoding="iso-8859-1")
                for offer in soup.findAll('a', href=True):
                    if len(self.offers[TYPES[(link.split('/'))[4]]]['links']) == 5:
                        continue
                    if TEMPLATE in offer['href']:
                        if offer['href'] not in self.offers[TYPES[(link.split('/'))[4]]]['links']:
                            self.offers[TYPES[(link.split('/'))[4]]]['links'].append(offer['href'])
            self.offers_len = self.offers_len + len(self.offers[TYPES[(link.split('/'))[4]]]['links'])

    def getoffers(self):
        for key in self.offers.keys():
            for offer in self.offers[key]['links']:
                self.result.append(self.find_values(offer, key, TEMP_ARR))

    def savetofile(self):
        with open(getFileName(OFFICE_PROPERTY['american']), WRITING_MODE, newline=NEWLINE, encoding=ENCODING) as f:
            writer = csv.DictWriter(f, delimiter=DELIMITER, fieldnames=HEADERS)
            writer.writerows(self.result)

    def run(self, root):
        self.countpages()
        self.searchoffers()
        self.progressBar = ProgressBar(root, self.offers_len)
        self.getoffers()
        self.savetofile()


def startAmerican(root):
    searcher = Searcher()
    searcher.run(root)
    createGlobalEstatesCsv()
