from consts import OFFICE_PROPERTY
from scrapers.future.future import Fetcher
from scrapers.future.write import write_to_file


def generateOnClickHandler(officeName):
    if officeName == OFFICE_PROPERTY['landowscy']:
        print('Wykonuje akcje dla biura Mikołaja')

    if officeName == OFFICE_PROPERTY['future']:
        fetcher = Fetcher()
        write_to_file(fetcher.get_offers('https://www.futurenieruchomosci.pl/lista-ofert?market=10') + fetcher.get_offers(
            'https://www.futurenieruchomosci.pl/lista-ofert?searchIndex=1&sort=add_date_desc&market=11'))
    if officeName == OFFICE_PROPERTY['level']:
        print('Wykonuje akcje dla biura Szymona')

    if officeName == OFFICE_PROPERTY['investor']:
        print('Wykonuje akcje dla biura Łukasza')

    if officeName == OFFICE_PROPERTY['american']:
        print('Wykonuje akcje dla biura Kacpra')
