import wx
from globalVariables import os, ROOT_DIR


class windowWithSinglePhoto(wx.Frame):
    def __init__(self, title, imageName, parent=None):
        image = wx.Image(os.path.join(ROOT_DIR + '/photos/' + imageName), wx.BITMAP_TYPE_ANY)
        wx.Frame.__init__(self, parent=parent, title=title)
        temp = image.ConvertToBitmap()
        size = temp.GetWidth(), temp.GetHeight()
        self.bmp = wx.StaticBitmap(parent=self, bitmap=temp)
        self.SetClientSize(size)
        self.Show()