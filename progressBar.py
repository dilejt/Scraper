import threading
from tkinter import *
from tkinter.ttk import Progressbar, Label


class ProgressBar:
    def __init__(self, root, maximum):
        self.iterable = DoubleVar()
        self.iterable.set(0)
        self.k = 0
        self.root = root
        self.maximum = maximum
        self.newWindow = Toplevel(root)
        self.newWindow.title('Generowanie')
        self.newWindow.resizable(False, False)
        self.newWindow.geometry('400x100')

        newFrame = Frame(self.newWindow)
        newFrame.pack()

        labelFrame = Frame(newFrame)
        labelFrame.pack(fill='x')

        self.progressLabel = Label(labelFrame, text=self.updateInfo())
        self.progressLabel.pack(side=TOP, padx=5, pady=5)

        progressbarFrame = Frame(newFrame)
        progressbarFrame.pack(fill='x')

        self.progressbar = Progressbar(
            progressbarFrame,
            length=300,
            orient='horizontal',
            mode='determinate',
            maximum=maximum
        )
        self.progressbar.pack(side=TOP, padx=5, pady=5)

        threading.Thread(target=self.progress()).start()

    def progress(self):
        if self.k < self.maximum:
            self.iterable.set(self.k)
            self.k += 1
            self.progressbar["value"] = self.k
            self.progressLabel['text'] = self.updateInfo()
            self.root.update_idletasks()
        else:
            self.stop()

    def stop(self):
        self.progressbar.stop()
        self.newWindow.destroy()

    def updateInfo(self):
        return "Pobieranie ofert" + ((self.k % 3 + 1) * ".") + ((3 - self.k % 3) * " ") + ' ' + str(int(self.k / self.maximum * 100)) + " %"
