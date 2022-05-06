from mainWindow import mainWindow, wx

if __name__ == '__main__':
    app = wx.App()
    frm = mainWindow(None)
    frm.Show()
    app.MainLoop()
