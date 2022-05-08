from tkinter import *
from consts import OFFICE_PROPERTY
from buttonMethods import generateOnClickHandler, filterOffers
from backend import getListEstates
from loader import Loader
from mainFrameMethods import addValidateOnInput, invalidateOffersFrame, invalidateNewOffersFrame


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
        offersLabel = Label(self.root, text="Oferty", font=("Arial", 16))
        offersLabel.grid(column=0, row=0, sticky=N, padx=5, pady=5)

        # grid(1,0)
        offersLabel = Label(self.root, text="Aktualności", font=("Arial", 16))
        offersLabel.grid(column=1, row=0, sticky=N, padx=5, pady=5)

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

        offersPriceLtInput = Entry(offersPriceFrame, width=5, validate="key")
        offersPriceLtInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(offersPriceLtInput)

        offersPriceSpaceLabel = Label(offersPriceFrame, text="zł -")
        offersPriceSpaceLabel.pack(side=LEFT, padx=0, pady=5)

        offersPriceGtInput = Entry(offersPriceFrame, width=5, validate="key")
        offersPriceGtInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(offersPriceGtInput)

        offersPriceEndingLabel = Label(offersPriceFrame, text="zł")
        offersPriceEndingLabel.pack(side=LEFT, padx=0, pady=5)

        offersLocalizationFrame = Frame(offersFilterFrame)
        offersLocalizationFrame.pack(fill='x')

        offersLocalizationLabel = Label(offersLocalizationFrame, text="Lokalizacja:", width="10", anchor="e")
        offersLocalizationLabel.pack(side=LEFT, padx=5, pady=5)

        offersLocalizationInput = Entry(offersLocalizationFrame, width=30)
        offersLocalizationInput.pack(side=LEFT, padx=5, pady=5)

        offersMarketFrame = Frame(offersFilterFrame)
        offersMarketFrame.pack(fill='x')

        offersAreaLabel = Label(offersMarketFrame, text="Rynek:", width="10", anchor="e")
        offersAreaLabel.pack(side=LEFT, padx=5, pady=5)

        offersMarketInput = Entry(offersMarketFrame, width=10)
        offersMarketInput.pack(side=LEFT, padx=5, pady=5)

        offersFilterFrame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        offersOfficeFrame = Frame(offersFilterFrame)
        offersOfficeFrame.pack(fill='x')

        offersOfficeLabel = Label(offersOfficeFrame, text="Biuro:", width="10", anchor="e")
        offersOfficeLabel.pack(side=LEFT, padx=5, pady=5)

        offersOfficeVariable = StringVar(offersOfficeFrame)

        offersOfficeDict = {'all': 'WSZYSTKIE'} | OFFICE_PROPERTY
        offersOfficeVariable.set(offersOfficeDict['all'])
        offersOfficeMenu = OptionMenu(offersOfficeFrame, offersOfficeVariable, *offersOfficeDict.values())

        offersOfficeMenu.config(width=15)
        offersOfficeMenu.pack(side=LEFT, padx=5, pady=5)

        offersFilterBtn = Button(offersOfficeFrame, text="Filtruj", command=lambda: filterOffers(
            self.root,
            offersLoader,
            offersTypeInput.get(),
            offersPriceLtInput.get(),
            offersPriceGtInput.get(),
            offersLocalizationInput.get(),
            offersMarketInput.get(),
            offersOfficeVariable.get()
        ))

        offersFilterBtn.pack(side=RIGHT, padx=5, pady=5)

        offersFilterFrame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        # grid(1,1) TODO
        newsFilterFrame = Frame(self.root)

        newsTypeFrame = Frame(newsFilterFrame)
        newsTypeFrame.pack(fill='x')

        newsTypeLabel = Label(newsTypeFrame, text="Typ:", width="10", anchor="e")
        newsTypeLabel.pack(side=LEFT, padx=5, pady=5)

        newsTypeInput = Entry(newsTypeFrame, width=30)

        newsTypeInput.pack(side=LEFT, padx=5, pady=5)

        newsPriceFrame = Frame(newsFilterFrame)
        newsPriceFrame.pack(fill='x')

        newsPriceLabel = Label(newsPriceFrame, text="Cena:", width="10", anchor="e")
        newsPriceLabel.pack(side=LEFT, padx=5, pady=5)

        newsPriceLtInput = Entry(newsPriceFrame, width=5, validate="key")
        newsPriceLtInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(newsPriceLtInput)

        newsPriceSpaceLabel = Label(newsPriceFrame, text="zł -")
        newsPriceSpaceLabel.pack(side=LEFT, padx=0, pady=5)

        newsPriceGtInput = Entry(newsPriceFrame, width=5, validate="key")
        newsPriceGtInput.pack(side=LEFT, padx=5, pady=5)
        addValidateOnInput(newsPriceGtInput)

        newsPriceEndingLabel = Label(newsPriceFrame, text="zł")
        newsPriceEndingLabel.pack(side=LEFT, padx=0, pady=5)

        newsLocalizationFrame = Frame(newsFilterFrame)
        newsLocalizationFrame.pack(fill='x')

        newsLocalizationLabel = Label(newsLocalizationFrame, text="Lokalizacja:", width="10", anchor="e")
        newsLocalizationLabel.pack(side=LEFT, padx=5, pady=5)

        newsLocalizationInput = Entry(newsLocalizationFrame, width=30)
        newsLocalizationInput.pack(side=LEFT, padx=5, pady=5)

        newsMarketFrame = Frame(newsFilterFrame)
        newsMarketFrame.pack(fill='x')

        newsAreaLabel = Label(newsMarketFrame, text="Rynek:", width="10", anchor="e")
        newsAreaLabel.pack(side=LEFT, padx=5, pady=5)

        newsMarketInput = Entry(newsMarketFrame, width=10)
        newsMarketInput.pack(side=LEFT, padx=5, pady=5)

        newsFilterFrame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        newsOfficeFrame = Frame(newsFilterFrame)
        newsOfficeFrame.pack(fill='x')

        newsOfficeLabel = Label(newsOfficeFrame, text="Biuro:", width="10", anchor="e")
        newsOfficeLabel.pack(side=LEFT, padx=5, pady=5)

        newsOfficeVariable = StringVar(newsOfficeFrame)

        newsOfficeDict = {'all': 'WSZYSTKIE'} | OFFICE_PROPERTY
        newsOfficeVariable.set(newsOfficeDict['all'])
        newsOfficeMenu = OptionMenu(newsOfficeFrame, newsOfficeVariable, *newsOfficeDict.values())

        newsOfficeMenu.config(width=15)
        newsOfficeMenu.pack(side=LEFT, padx=5, pady=5)

        newsFilterBtn = Button(newsOfficeFrame, text="Filtruj", command=lambda: filterOffers(
            self.root,
            newsLoader,
            newsTypeInput.get(),
            newsPriceLtInput.get(),
            newsPriceGtInput.get(),
            newsLocalizationInput.get(),
            newsMarketInput.get(),
            newsOfficeVariable.get()
        ))

        newsFilterBtn.pack(side=RIGHT, padx=5, pady=5)

        newsFilterFrame.grid(column=1, row=1, sticky=W, padx=5, pady=5)

        # grid(0,2)
        offersLoaderFrame = Frame(self.root)
        offersLoader = Loader(offersLoaderFrame)
        offersLoaderFrame.grid(column=0, row=2, sticky=N, padx=5, pady=5)

        # grid(1,2) TODO
        newsLoaderFrame = Frame(self.root)
        newsLoader = Loader(newsLoaderFrame)
        newsLoaderFrame.grid(column=1, row=2, sticky=N, padx=5, pady=5)

        # grid(0,3)
        getListEstates()
        invalidateOffersFrame(self.root, offersLoader)

        # grid(1,3)
        invalidateNewOffersFrame(self.root, offersLoader)

        # grid(2,3)
        buttonFrame = Frame(self.root)

        variable = StringVar(buttonFrame)
        variable.set(OFFICE_PROPERTY['landowscy'])
        optionMenu = OptionMenu(buttonFrame, variable, *OFFICE_PROPERTY.values())
        optionMenu.config(width=14)
        optionMenu.grid(column=0, row=0, sticky=N, padx=5, pady=5)

        generateBtn = Button(buttonFrame, text="Generuj", width=10,
                             command=lambda: generateOnClickHandler(variable.get(), self.root, offersLoader))
        generateBtn.grid(column=0, row=1, sticky=N, padx=5, pady=5)

        mergeBtn = Button(buttonFrame, text="Łączenie", width=10)
        mergeBtn.grid(column=0, row=2, sticky=N, padx=5, pady=5)

        filesBtn = Button(buttonFrame, text="Pliki...", width=10)
        filesBtn.grid(column=0, row=3, sticky=N, padx=5, pady=5)

        buttonFrame.grid(column=2, row=3, sticky=N, padx=5, pady=5)
