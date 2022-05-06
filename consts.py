import os

# przyklad poslugiwania sie dict: OFFICE_PROPERTY['landowscy'] wyswietli: 'LANDOWSCY'
OFFICE_PROPERTY = {'landowscy': 'LANDOWSCY', 'future': 'FUTURE', 'level': 'LEVEL', 'investor': 'Investor', 'american': 'AmericanHome'}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY_TO_SAVE_CSV = 'data'

ENCODING = "utf-8"
NEWLINE = ''
WRITING_MODE = 'w'
DELIMITER = ';'
