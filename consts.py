import os

# przyklad poslugiwania sie dict: OFFICE_PROPERTY['landowscy'] wyswietli: 'LANDOWSCY'
OFFICE_PROPERTY = {'landowscy': 'LANDOWSCY', 'future': 'FUTURE', 'level': 'LEVEL', 'investor': 'Investor', 'american': 'AmericanHome'}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
NEW_ESTATES_CSV = os.path.join(ROOT_DIR, os.path.basename('newGlobalEstates' + '.csv'))
OLD_ESTATES_CSV = os.path.join(ROOT_DIR, os.path.basename('oldGlobalEstates' + '.csv'))

DIRECTORY_TO_SAVE_CSV = 'data'

ENCODING = "utf-8"
NEWLINE = ''
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
