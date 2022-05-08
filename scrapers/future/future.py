import datetime
import re

from backend import updateOffers
from consts import HEADERS
from progressBar import ProgressBar
from scrapers.future.fields import FIELD_RELATIONS
from scrapers.future.myhelpers import get_soup, format_string, get_len_offers
from scrapers.future.write import write_to_file


class Fetcher:
    def __init__(self, progressBar):
        self.progressBar = progressBar
        self.result_dict = None

    def get_offers(self, url):
        self.result_dict = []
        next_url = None
        self.scrap_offer(url)
        while True:
            if next_url is None:
                soup = get_soup(url)
            else:
                soup = get_soup(next_url)
            next_page = soup.select_one(".pagination-next")
            if next_page is None:
                break
            else:
                next_url = next_page['href']
                self.scrap_offer(next_url)
        return self.result_dict

    def scrap_offer(self, url):
        page_result = []
        soup = get_soup(url)
        for offer in soup.select(".background-white-list-offer"):
            existing_fields = []
            result = []
            carousel = offer.select_one(".carousel-inner")
            btn = offer.select_one(".list-offer-btn")
            street = offer.select_one(".list-title-street")
            soup = get_soup(btn['href'])
            get_fields_inside(soup, existing_fields)
            # link
            existing_fields.append(["link", btn['href']])
            # liczba_zdjec, zdjecia_linki, zdjecie_glowne, zdjecie_glowne_link
            span = offer.select_one(".no-padding").find("span")
            link = re.search('\'(.+?)\'', span['style']).group(1)
            if carousel is None:
                existing_fields.append(["liczba_zdjec", "1"])
                existing_fields.append(["zdjecia_linki", link])
                existing_fields.append(["zdjecie_glowne", link])
                existing_fields.append(["zdjecie_glowne_link", link])
            else:
                existing_fields.append(["liczba_zdjec", len(carousel.select('.item'))])
                existing_fields.append(
                    ["zdjecia_linki", [re.search('\'(.+?)\'', item.find("span")['style']).group(1) for item in carousel.select('.item')]])
                existing_fields.append(["zdjecie_glowne", link])
                existing_fields.append(["zdjecie_glowne_link", link])

            # lokalizacja
            if street is not None:
                existing_fields.append(["lokalizacja", offer.select_one(".list-title:has(span)").get_text().strip() + ' ' + street.get_text()])
            else:
                existing_fields.append(["lokalizacja", offer.select_one(".list-title:has(span)").get_text().strip()])
            # rynek
            if "market=10" in url:
                existing_fields.append(["rynek", "piewotny"])
            elif "market=11" in url:
                existing_fields.append(["rynek", "wtórny"])
            # nazwa_biura
            existing_fields.append(["nazwa_biura", "futurenieruchomosci"])
            # data_skanowania
            existing_fields.append(["data_skanowania", datetime.datetime.now()])

            for field in HEADERS:
                if field not in [element[0] for element in existing_fields]:
                    result.append('-1')
                else:
                    result.append([element[1] for element in existing_fields if element[0] == field][0])
            print(result)
            page_result.append(result)
            self.progressBar.progress()
        self.result_dict += page_result


def get_fields_inside(soup, existing_fields):
    # powierzchnia, powierzchnia dzialki, pietro, budynek_pietra, cena, cena za m2, rok budowy, numer oferty, liczba pokoi
    for td in soup.select(".table > tbody > tr"):
        # check if field exists in file
        field_name = format_string(td.select_one(".offer-data").get_text())
        if field_name not in [list(element.keys())[0] for element in FIELD_RELATIONS]:
            continue  # jasna kuchnia, ogrzewanie
        value = td.select_one(".offer-data-values").get_text()
        field_relation_name = FIELD_RELATIONS[[list(element.keys())[0] for element in FIELD_RELATIONS].index(field_name)].get(field_name)
        if "pietro" == field_relation_name and not format_string(value).find('z') == -1:
            existing_fields.append([field_relation_name, format_string(value)[0:format_string(value).find('z')]])
            existing_fields.append(["budynek_pietra", format_string(value)[format_string(value).find('z') + 1:]])
        elif "cena" in field_relation_name:
            existing_fields.append([field_relation_name, format(float(format_string(value).replace("PLN", "")), '.2f')])
        elif "powierzchnia" in field_relation_name:
            existing_fields.append([field_relation_name, format_string(value).replace("m2", "")])
        elif "balkon" in field_relation_name:
            existing_fields.append([field_relation_name, True])
        else:
            existing_fields.append([field_relation_name, format_string(value)])
    # typ transakcji
    if "sprzedaż" in format_string(soup.select_one('.box-area').get_text()):
        existing_fields.append(["typ_transakcji", "Sprzedaż"])
    elif "wynajem" in format_string(soup.select_one('.box-area').get_text()):
        existing_fields.append(["typ_transakcji", "Wynajem"])
    # typ
    building_type = soup.select_one('.box-area').get_text().encode('ISO-8859-2', 'ignore').decode('ISO-8859-2')
    existing_fields.append(["typ", building_type[0:building_type.find('na ') - 1]])
    # telefon
    existing_fields.append(
        ["telefon", format_string(soup.select_one("#phone .icon-text-position").get_text()).replace('Telefon:', '').replace(',', '|')])
    # email
    existing_fields.append(["email", format_string(soup.select(".icon-text-position")[1].get_text())])
    # opis
    description = soup.select_one(".offer-detailed").get_text().encode('ISO-8859-2', 'ignore').decode('ISO-8859-2')
    existing_fields.append(["opis", description])
    # winda
    if re.search('wind.?', description, re.IGNORECASE):
        existing_fields.append(["winda", True])
    # standard_wykończenia
    if re.search('pod.klucz', description, re.IGNORECASE):
        existing_fields.append(["standard_wykonczenia", "pod klucz"])
    elif re.search('stan. deweloperski', description, re.IGNORECASE):
        existing_fields.append(["standard_wykonczenia", "deweloperski"])
    # piwnica
    if re.search('piwnic.?', description, re.IGNORECASE):
        existing_fields.append(["piwnica", True])
    # umeblowane
    if re.search('u?mebl\w*', description, re.IGNORECASE):
        existing_fields.append(["umeblowane", True])
    # kaucja
    deposit = re.search('Kaucj. gwaryncyjn. w wysoko.ci \d+\W?\d+|Jednorazow. kaucj. zwrotn. w wysoko.ci \d+\W?\d+', description, re.IGNORECASE)
    if deposit is not None:
        existing_fields.append(
            ["kaucja", [int(word.replace(".", "")) for word in deposit.group(0).split() if word.replace(".", "").isdigit()][0]])


def startFuture(root, loader):
    progressBar = ProgressBar(root, get_len_offers())
    fetcher = Fetcher(progressBar)
    write_to_file(fetcher.get_offers('https://www.futurenieruchomosci.pl/lista-ofert?market=10') + fetcher.get_offers(
        'https://www.futurenieruchomosci.pl/lista-ofert?searchIndex=1&sort=add_date_desc&market=11'))
    updateOffers(root, loader)
