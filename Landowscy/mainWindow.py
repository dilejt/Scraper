import wx.xrc
import wx.grid
import webbrowser
from methods import *
from photoViewer import photoViewer
from photoViewerFromFile import windowWithSinglePhoto


class mainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='Mikołaj Wesołek 18933 Internetowy Robot', pos=wx.DefaultPosition,
                          size=wx.Size(530, 264), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.Size(800, 600))
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))
        container = wx.BoxSizer(wx.VERTICAL)

        buttonContainer = wx.FlexGridSizer(10, 3, 12, 115)
        buttonContainer.SetFlexibleDirection(wx.BOTH)
        buttonContainer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        self.searchAndGenerateButton = wx.Button(self, wx.ID_ANY, u"Przeszukaj", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonContainer.Add(self.searchAndGenerateButton, 0, wx.ALL, 5)

        self.compareButton = wx.Button(self, wx.ID_ANY, u"Porównaj", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonContainer.Add(self.compareButton, 0, wx.ALL, 5)

        self.mergeButton = wx.Button(self, wx.ID_ANY, u"Połącz pliki csv", wx.DefaultPosition, wx.DefaultSize, 0)
        buttonContainer.Add(self.mergeButton, 0, wx.ALL, 5)

        container.Add(buttonContainer, 1, wx.EXPAND, 5)

        labelContainer = wx.BoxSizer(wx.VERTICAL)

        labelContainer.SetMinSize(wx.Size(200, -1))
        self.label = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize,
                                   wx.ALIGN_CENTER_HORIZONTAL)
        self.label.Wrap(-1)

        self.label.SetFont(
            wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_HEAVY, False, "Arial Black"))
        self.label.SetMinSize(wx.Size(500, -1))

        labelContainer.Add(self.label, 0, wx.ALL, 5)

        container.Add(labelContainer, 1, wx.EXPAND, 5)

        gridContainer = wx.BoxSizer(wx.VERTICAL)

        self.dataGrid = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid

        gridContainer.Add(self.dataGrid, 0, wx.ALL, 5)

        container.Add(gridContainer, 1, wx.EXPAND, 5)

        self.SetSizer(container)
        self.Layout()
        self.dataGrid.Hide()

        self.Centre(wx.BOTH)

        # Connect Events
        self.searchAndGenerateButton.Bind(wx.EVT_BUTTON, self.searchAndGenerateButtonOnButtonClick)
        self.compareButton.Bind(wx.EVT_BUTTON, self.compareButtonOnButtonClick)
        self.mergeButton.Bind(wx.EVT_BUTTON, self.mergeButtonOnButtonClick)

        self.dataGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.dataGridOnGridCellLeftClick)
        self.mainPhotoArray = []
        self.photosLink = []
        self.isGridCreated = False
        self.numberOfRows = 0

    def __del__(self):
        pass

    def refresh(self):
        x, y = self.GetSize()
        self.SetSize((x, y + 1))
        self.SetSize((x, y))

    def renderTable(self, fieldNamesList, currentFileDict):
        if not self.isGridCreated:
            self.numberOfRows = len(currentFileDict)
            self.dataGrid.CreateGrid(len(currentFileDict), len(fieldNamesList))
        else:
            self.dataGrid.DeleteRows(pos=0, numRows=self.numberOfRows, updateLabels=True)
            self.dataGrid.AppendRows(len(currentFileDict))
        self.isGridCreated = True
        self.dataGrid.EnableEditing(False)
        self.dataGrid.EnableGridLines(True)
        self.dataGrid.SetGridLineColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.dataGrid.EnableDragGridSize(False)
        self.dataGrid.SetMargins(0, 0)

        # Columns
        self.dataGrid.EnableDragColMove(False)
        self.dataGrid.EnableDragColSize(True)
        self.dataGrid.SetDefaultColSize(120, resizeExistingCols=True)
        self.dataGrid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.dataGrid.AutoSizeRows()
        self.dataGrid.EnableDragRowSize(True)
        self.dataGrid.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Label Appearance
        self.dataGrid.SetLabelBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.dataGrid.SetLabelTextColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        # Cell Defaults
        self.dataGrid.SetDefaultCellBackgroundColour(wx.Colour(170, 205, 240))
        self.dataGrid.SetDefaultCellTextColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        self.dataGrid.SetDefaultCellFont(
            wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.dataGrid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        counter = 0
        rowNumber = 0
        self.photosLink = []
        self.mainPhotoArray = []
        for item in fieldNamesList:
            self.dataGrid.SetColLabelValue(counter, item)
            counter += 1
        for offer in currentFileDict:
            columnNumber = 0
            for offerField in offer:
                cellValue = str(offer[offerField])
                if columnNumber == 6 or columnNumber == 10:
                    self.dataGrid.SetCellFont(rowNumber, columnNumber,
                                              wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                                                      True, "Arial"))
                if columnNumber == 8:
                    self.photosLink.append(cellValue.replace('[', '').replace(']', '').split(','))
                    cellValue = 'OBEJRZYJ ZDJECIA'
                if columnNumber == 9:
                    self.mainPhotoArray.append(cellValue)
                    cellValue = 'ZOBACZ'
                self.dataGrid.SetCellValue(rowNumber, columnNumber, cellValue)
                columnNumber += 1
            rowNumber += 1
        self.dataGrid.Show()
        self.refresh()

    def searchAndGenerateButtonOnButtonClick(self, event):
        if self.isGridCreated:
            self.dataGrid.Hide()
        self.label.SetLabelText("Przeszukuje liste ofert landowscy-nieruchomosci.pl")
        searchOffers('/lista-ofert/')
        self.label.SetLabelText("Sprawdzam dostępne oferty...")
        processOffers(self.label.SetLabelText)
        self.label.SetLabelText("Zapisuje znalezione oferty do pliku .csv")
        fieldNamesList = []
        for field in fieldNamesDict:
            fieldNamesList.append(fieldNamesDict[field])
        fileNameCurrentOffer = 'offers_list_' + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + '.csv'
        directoryCurrentOffer = 'csv'
        generateCsvFile(offerList, fieldNamesList, directoryCurrentOffer, fileNameCurrentOffer)
        self.label.SetLabelText("Wczytuje zapisany plik: " + fileNameCurrentOffer)
        listOfCsvFilesToCompare = newestFiles(os.path.join(ROOT_DIR + '/csv'))
        currentFilePath = listOfCsvFilesToCompare[:1]
        currentFileDict = readCsv(currentFilePath[0])
        if len(currentFileDict) > 0:
            self.renderTable(fieldNamesList, currentFileDict)
            self.label.SetLabelText("Znaleziono następujące oferty("+str(len(currentFileDict))+"):")
        else:
            self.label.SetLabelText("Nie znaleziono ofert:")
        event.Skip()

    def compareButtonOnButtonClick(self, event):
        if self.isGridCreated:
            self.dataGrid.Hide()
        self.label.SetLabelText("Porownuje dwie ostatnie listy ofert")
        listOfCsvFilesToCompare = newestFiles(os.path.join(ROOT_DIR + '/csv'))
        currentFilePath, lastFilePath = listOfCsvFilesToCompare[:2]
        self.label.SetLabelText("Odczytuje pierwszy plik")
        currentFileDict = readCsv(currentFilePath)
        self.label.SetLabelText("Odczytuje drugi plik")
        lastFileDict = readCsv(lastFilePath)
        self.label.SetLabelText("Znajduje najnowsze oferty")
        newOffers = getNewOffers(currentFileDict, lastFileDict)
        fieldNamesList = []
        for field in fieldNamesDict:
            fieldNamesList.append(fieldNamesDict[field])
        if len(newOffers) > 0:
            self.renderTable(fieldNamesList, newOffers)
            self.label.SetLabelText("Pojawily sie nowe oferty("+str(len(newOffers))+"):")
        else:
            self.label.SetLabelText("Niestety nie znaleziono nowych ofert")
        event.Skip()

    def mergeButtonOnButtonClick(self, event):
        if self.isGridCreated:
            self.dataGrid.Hide()
        self.label.SetLabelText("Dodaje pliki do zmergowania")
        listOfCsvFilesToMerge = newestFiles(os.path.join(ROOT_DIR + '/csvToMerge'))
        fieldNamesList = []
        for field in fieldNamesDict:
            fieldNamesList.append(fieldNamesDict[field])
        self.label.SetLabelText("Rozpoczynam laczenie plikow")
        mergedOffersDict = mergeFiles(fieldNamesList, listOfCsvFilesToMerge)
        if len(mergedOffersDict) > 0:
            self.renderTable(fieldNamesList, mergedOffersDict)
            self.label.SetLabelText("Wyswietlam polaczone oferty (" + str(len(mergedOffersDict))+" ofert):")
        else:
            self.label.SetLabelText("cos poszlo nie tak :(")
        event.Skip()

    def dataGridOnGridCellLeftClick(self, event):
        colNumber = event.GetCol()
        rowNumber = event.GetRow()
        if colNumber == 6 or colNumber == 10:
            text = self.dataGrid.GetCellValue(rowNumber, colNumber)
            webbrowser.open_new_tab(text)
        if colNumber == 8:
            photoViewer(title='Photo Viewer', imageArray=self.photosLink[rowNumber])
        if colNumber == 9:
            windowWithSinglePhoto(title='Main Photo From Offer', imageName=self.mainPhotoArray[rowNumber])
        event.Skip()

