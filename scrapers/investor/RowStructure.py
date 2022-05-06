class RowStructure:
    def __init__(self):
        self.typ = -1
        self.cena = -1
        self.typ_transakcji = -1
        self.dostepny = -1
        self.powierzchnia = -1
        self.powierzchnia_dzialki = -1
        self.link = -1
        self.liczba_zdjec = -1
        self.zdjecia_linki = -1
        self.zdjecie_glowne = -1
        self.zdjecie_glowne_link = -1
        self.opis = -1
        self.rynek = -1
        self.liczba_pomieszczen = -1
        self.pietro = -1
        self.lokalizacja = -1
        self.cena_za_m2 = -1
        self.typ_zabudowy = -1
        self.standard_wykonczenia = -1
        self.rok_budowy = -1
        self.balkon = -1
        self.miejsce_parkingowe = -1
        self.winda = -1
        self.stan_wykonczenia = -1
        self.piwnica = -1
        self.umeblowane = -1
        self.liczba_lazienek = -1
        self.numer_oferty = -1
        self.lokale_uzytkowe = -1
        self.oplaty = -1
        self.nr_oferty = -1
        self.budynek_pietra = -1
        self.kaucja = -1
        self.wystawa_okien = -1
        self.dojazd = -1
        self.stan_prawny_dzialki = -1
        self.telefon = -1
        self.email = -1
        self.nazwa_biura = -1
        self.data_dodania_oferty = -1
        self.data_skanowania = -1

    def set_typ(self, x):
        self.typ = x

    def set_cena(self, x):
        self.cena = x

    def set_typ_transakcji(self, x):
        self.typ_transakcji = x

    def set_dostepny(self, x):
        self.dostepny = x

    def set_powierzchnia(self, x):
        self.powierzchnia = x

    def set_powierzchnia_dzialki(self, x):
        self.powierzchnia_dzialki = x

    def set_link(self, x):
        self.link = x

    def set_liczba_zdjec(self, x):
        self.liczba_zdjec = x

    def set_zdjecia_linki(self, x):
        self.zdjecia_linki = x

    def set_zdjecie_glowne(self, x):
        self.zdjecie_glowne = x

    def set_zdjecie_glowne_link(self, x):
        self.zdjecie_glowne_link = x

    def set_opis(self, x):
        self.opis = x

    def set_rynek(self, x):
        self.rynek = x

    def set_liczba_pomieszczen(self, x):
        self.liczba_pomieszczen = x

    def set_pietro(self, x):
        self.pietro = x

    def set_lokalizacja(self, x):
        self.lokalizacja = x

    def set_cena_za_m2(self, x):
        self.cena_za_m2 = x

    def set_typ_zabudowy(self, x):
        self.typ_zabudowy = x

    def set_standard_wykonczenia(self, x):
        self.standard_wykonczenia = x

    def set_rok_budowy(self, x):
        self.rok_budowy = x

    def set_balkon(self, x):
        self.balkon = x

    def set_miejsce_parkingowe(self, x):
        self.miejsce_parkingowe = x

    def set_winda(self, x):
        self.winda = x

    def set_stan_wykonczenia(self, x):
        self.stan_wykonczenia = x

    def set_piwnica(self, x):
        self.piwnica = x

    def set_umeblowane(self, x):
        self.umeblowane = x

    def set_liczba_lazienek(self, x):
        self.liczba_lazienek = x

    def set_numer_oferty(self, x):
        self.numer_oferty = x

    def set_lokale_uzytkowe(self, x):
        self.lokale_uzytkowe = x

    def set_oplaty(self, x):
        self.oplaty = x

    def set_nr_oferty(self, x):
        self.nr_oferty = x

    def set_budynek_pietra(self, x):
        self.budynek_pietra = x

    def set_kaucja(self, x):
        self.kaucja = x

    def set_wystawa_okien(self, x):
        self.wystawa_okien = x

    def set_dojazd(self, x):
        self.dojazd = x

    def set_stan_prawny_dzialki(self, x):
        self.stan_prawny_dzialki = x

    def set_telefon(self, x):
        self.telefon = x

    def set_email(self, x):
        self.email = x

    def set_nazwa_biura(self, x):
        self.nazwa_biura = x

    def set_data_dodania_oferty(self, x):
        self.data_dodania_oferty = x

    def set_data_skanowania(self, x):
        self.data_skanowania = x

    def toArray(self):
        return [
            self.typ,
            self.cena,
            self.typ_transakcji,
            self.dostepny,
            self.powierzchnia,
            self.powierzchnia_dzialki,
            self.link,
            self.liczba_zdjec,
            self.zdjecia_linki,
            self.zdjecie_glowne,
            self.zdjecie_glowne_link,
            self.opis,
            self.rynek,
            self.liczba_pomieszczen,
            self.pietro,
            self.lokalizacja,
            self.cena_za_m2,
            self.typ_zabudowy,
            self.standard_wykonczenia,
            self.rok_budowy,
            self.balkon,
            self.miejsce_parkingowe,
            self.winda,
            self.stan_wykonczenia,
            self.piwnica,
            self.umeblowane,
            self.liczba_lazienek,
            self.numer_oferty,
            self.lokale_uzytkowe,
            self.oplaty,
            self.nr_oferty,
            self.budynek_pietra,
            self.kaucja,
            self.wystawa_okien,
            self.dojazd,
            self.stan_prawny_dzialki,
            self.telefon,
            self.email,
            self.nazwa_biura,
            self.data_dodania_oferty,
            self.data_skanowania
        ]