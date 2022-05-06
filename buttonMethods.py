from consts import OFFICE_PROPERTY


def generateOnClickHandler(officeName):
    if officeName == OFFICE_PROPERTY['landowscy']:
        print('Wykonuje akcje dla biura Mikołaja')

    if officeName == OFFICE_PROPERTY['future']:
        print('Wykonuje akcje dla biura Damiana')

    if officeName == OFFICE_PROPERTY['level']:
        print('Wykonuje akcje dla biura Szymona')

    if officeName == OFFICE_PROPERTY['investor']:
        print('Wykonuje akcje dla biura Łukasza')

    if officeName == OFFICE_PROPERTY['american']:
        print('Wykonuje akcje dla biura Kacpra')
