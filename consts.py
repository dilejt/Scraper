import os
from pathlib import Path

offersList = []
filteredOferList = []
newOfferList = []
newFilteredOfferList = []

OFFICE_PROPERTY = {'landowscy': 'LANDOWSCY', 'future': 'FUTURE', 'level': 'LEVEL', 'investor': 'Investor', 'american': 'AmericanHome'}

DIRECTORY_TO_SAVE_CSV = 'data'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

NEW_ESTATES_CSV = os.path.join(ROOT_DIR, os.path.basename('newGlobalEstates' + '.csv'))
OLD_ESTATES_CSV = os.path.join(ROOT_DIR, os.path.basename('oldGlobalEstates' + '.csv'))

AMERICAN_DATA_DIRECTORY = os.path.join(ROOT_DIR, DIRECTORY_TO_SAVE_CSV, OFFICE_PROPERTY['american'])
FUTURE_DATA_DIRECTORY = os.path.join(ROOT_DIR, DIRECTORY_TO_SAVE_CSV, OFFICE_PROPERTY['future'])
INVESTOR_DATA_DIRECTORY = os.path.join(ROOT_DIR, DIRECTORY_TO_SAVE_CSV, OFFICE_PROPERTY['investor'])
LANDOWSCY_DATA_DIRECTORY = os.path.join(ROOT_DIR, DIRECTORY_TO_SAVE_CSV, OFFICE_PROPERTY['landowscy'])
LEVEL_DATA_DIRECTORY = os.path.join(ROOT_DIR, DIRECTORY_TO_SAVE_CSV, OFFICE_PROPERTY['level'])

ENCODING = "utf-8"
NEWLINE = ''
READ_MODE = 'r'
WRITING_MODE = 'w'
DELIMITER = ';'

HEADERS = [
    'typ',
    'cena',
    'typ_transakcji',
    'dostepny',
    'powierzchnia',
    'powierzchnia_dzialki',
    'link',
    'liczba_zdjec',
    'zdjecia_linki',
    'zdjecie_glowne',
    'zdjecie_glowne_link',
    'opis',
    'rynek',
    'liczba_pomieszczen',
    'pietro',
    'lokalizacja',
    'cena_za_m2',
    'typ_zabudowy',
    'standard_wykonczenia',
    'rok_budowy',
    'balkon',
    'miejsce_parkingowe',
    'winda',
    'stan_wykonczenia',
    'piwnica',
    'umeblowane',
    'liczba_lazienek',
    'numer_oferty',
    'lokale_uzytkowe',
    'oplaty',
    'nr_oferty',
    'budynek_pietra',
    'kaucja',
    'wystawa_okien',
    'dojazd',
    'stan_prawny_dzialki',
    'telefon',
    'email',
    'nazwa_biura',
    'data_dodania_oferty',
    'data_skanowania'
]

filterKeyDict = {
    'type': 'type',
    'priceMin': 'priceMin',
    'priceMax': 'priceMax',
    'localization': 'localization',
    'market': 'market',
    'office': 'office',
}