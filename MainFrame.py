from tkinter import *
from consts import OFFICE_PROPERTY
from buttonMethods import generateOnClickHandler, filterOffers
from backend import getListEstates, getListComparedEstates
from mainFrameMethods import createList, addValidateOnInput


class MainFrame:
    def __init__(self):
        self.root = Tk()
        self.root.title("Scrapers")
        self.initMainGui()
        mainloop()

    def initMainGui(self):
        self.root.columnconfigure(0, weight=5)
        self.root.columnconfigure(1, weight=5)
        self.root.columnconfigure(2, weight=2)

        # grid(0,0)
        offersLabel = Label(self.root, text="Oferty")
        offersLabel.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        # grid(1,0)
        offersLabel = Label(self.root, text="Aktualności")
        offersLabel.grid(column=1, row=0, sticky=W, padx=5, pady=5)

        # grid(0,1)
        offersFilterFrame = Frame(self.root)

        offersTypeFrame = Frame(offersFilterFrame)
        offersTypeFrame.pack(fill='x')

        offersTypeLabel = Label(offersTypeFrame, text="Typ:", width="10", anchor="e")
        offersTypeLabel.pack(side=LEFT, padx=5, pady=5)

        offersTypeInput = Entry(offersTypeFrame, width=30)
        offersTypeInput.pack(side=LEFT, padx=5, pady=5)

        offersPriceFrame = Frame(offersFilterFrame)
        offersPriceFrame.pack(fill='x')

        offersPriceLabel = Label(offersPriceFrame, text="Cena:", width="10", anchor="e")
        offersPriceLabel.pack(side=LEFT, padx=5, pady=5)

        offersPriceGtInput = Entry(offersPriceFrame, width=5, validate="key")
        offersPriceGtInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(offersPriceGtInput)

        offersPriceSpaceLabel = Label(offersPriceFrame, text="zł -")
        offersPriceSpaceLabel.pack(side=LEFT, padx=0, pady=5)

        offersPriceLtInput = Entry(offersPriceFrame, width=5, validate="key")
        offersPriceLtInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(offersPriceLtInput)

        offersPriceEndingLabel = Label(offersPriceFrame, text="zł")
        offersPriceEndingLabel.pack(side=LEFT, padx=0, pady=5)

        offersLocalizationFrame = Frame(offersFilterFrame)
        offersLocalizationFrame.pack(fill='x')

        offersLocalizationLabel = Label(offersLocalizationFrame, text="Lokalizacja:", width="10", anchor="e")
        offersLocalizationLabel.pack(side=LEFT, padx=5, pady=5)

        offersLocalizationInput = Entry(offersLocalizationFrame, width=30)
        offersLocalizationInput.pack(side=LEFT, padx=5, pady=5)

        offersAreaFrame = Frame(offersFilterFrame)
        offersAreaFrame.pack(fill='x')

        offersAreaLabel = Label(offersAreaFrame, text="Powierzchnia:", width="10", anchor="e")
        offersAreaLabel.pack(side=LEFT, padx=5, pady=5)

        offersAreaInput = Entry(offersAreaFrame, width=10, validate="key")
        offersAreaInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(offersAreaInput)

        offersFilterFrame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        offersOfficeFrame = Frame(offersFilterFrame)
        offersOfficeFrame.pack(fill='x')

        offersOfficeLabel = Label(offersOfficeFrame, text="Biuro:", width="10", anchor="e")
        offersOfficeLabel.pack(side=LEFT, padx=5, pady=5)

        offersOfficeVariable = StringVar(offersOfficeFrame)
        offersOfficeVariable.set("1")
        offersOfficeMenu = OptionMenu(offersOfficeFrame, offersOfficeVariable, "1", "2", "3", "4", "5")
        offersOfficeMenu.config(width=7)
        offersOfficeMenu.pack(side=LEFT, padx=5, pady=5)

        offersFilterBtn = Button(offersOfficeFrame, text="Filtruj", command=lambda: filterOffers())
        offersFilterBtn.pack(side=RIGHT, padx=5, pady=5)

        offersFilterFrame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        # grid(1,1) TODO

        # grid(0,2) todo dodac jako 2 parametr zassane dane z global csv'ki
        offersTable = createList(self.root, getListEstates())
        offersTable.grid(column=0, row=2, sticky=W, padx=5, pady=5)

        # grid(1,2)
        updatesTable = createList(self.root, getListComparedEstates())
        updatesTable.grid(column=1, row=2, sticky=W, padx=5, pady=5)

        # grid(2,2)
        buttonFrame = Frame(self.root)

        variable = StringVar(buttonFrame)
        variable.set(OFFICE_PROPERTY['landowscy'])
        optionMenu = OptionMenu(buttonFrame, variable, *OFFICE_PROPERTY.values())
        optionMenu.config(width=12)
        optionMenu.grid(column=0, row=0, sticky=N, padx=5, pady=5)

        generateBtn = Button(buttonFrame, text="Generuj", width=10,
                             command=lambda: generateOnClickHandler(variable.get()))
        generateBtn.grid(column=0, row=1, sticky=N, padx=5, pady=5)

        mergeBtn = Button(buttonFrame, text="Łączenie", width=10)
        mergeBtn.grid(column=0, row=2, sticky=N, padx=5, pady=5)

        filesBtn = Button(buttonFrame, text="Pliki...", width=10)
        filesBtn.grid(column=0, row=3, sticky=N, padx=5, pady=5)

        buttonFrame.grid(column=2, row=2, sticky=N, padx=5, pady=5)