import io
import urllib.parse
import urllib.request
import wx

class photoViewer(wx.Frame):
    def __init__(self, title, imageArray, parent=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.photosArray = imageArray
        self.photoIndex = 0
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        container = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        topContainer = wx.BoxSizer(wx.VERTICAL)

        self.bmp = self.getPhotoFromUrl(self.photosArray[self.photoIndex])

        topContainer.Add(self.bmp, 0, wx.ALL, 5)

        container.Add(topContainer, 1, wx.EXPAND, 5)

        bottomContainer = wx.BoxSizer(wx.HORIZONTAL)

        self.prevPhoto = wx.Button(self, wx.ID_ANY, u"Poprzednie", wx.DefaultPosition, wx.DefaultSize, 0)
        bottomContainer.Add(self.prevPhoto, 0, wx.ALL, 5)

        self.photoIndexLabel = wx.StaticText(self, wx.ID_ANY, u"1/"+str(len(imageArray)), wx.DefaultPosition, wx.DefaultSize, 0)
        self.photoIndexLabel.Wrap(-1)

        bottomContainer.Add(self.photoIndexLabel, 0, wx.ALL, 5)

        self.nextPhoto = wx.Button(self, wx.ID_ANY, u"Nastepne", wx.DefaultPosition, wx.DefaultSize, 0)
        bottomContainer.Add(self.nextPhoto, 0, wx.ALL, 5)

        container.Add(bottomContainer, 1, wx.EXPAND, 5)

        self.SetSizer(container)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.prevPhoto.Bind(wx.EVT_BUTTON, self.prevPhotoOnButtonClick)
        self.nextPhoto.Bind(wx.EVT_BUTTON, self.nextPhotoOnButtonClick)

        self.Show()

    def __del__(self):
        pass

    def getPhotoFromUrl(self, imgUrl):
        content = urllib.request.urlopen(imgUrl.replace("'", "")).read()
        io_bytes = io.BytesIO(content)
        image = wx.Image(io_bytes).ConvertToBitmap()
        size = image.GetWidth(), image.GetHeight() + 50
        self.SetClientSize(size)
        return wx.StaticBitmap(parent=self, bitmap=image)

    def prevPhotoOnButtonClick(self, event):
        self.photoIndex -= 1
        if self.photoIndex < 0:
            self.photoIndex = len(self.photosArray) - 1
        self.bmp = self.getPhotoFromUrl(self.photosArray[self.photoIndex])
        self.photoIndexLabel.SetLabelText(str(self.photoIndex + 1)+"/"+str(len(self.photosArray)))
        event.Skip()

    def nextPhotoOnButtonClick(self, event):
        self.photoIndex += 1
        if self.photoIndex == len(self.photosArray):
            self.photoIndex = 0
        self.bmp = self.getPhotoFromUrl(self.photosArray[self.photoIndex])
        self.photoIndexLabel.SetLabelText(str(self.photoIndex + 1) + "/" + str(len(self.photosArray)))
        event.Skip()

