from tkinter import Label


class Loader:
    def __init__(self, frame):
        self.isLoading = True
        self.frame = frame
        self.startLoading()

    def startLoading(self):
        self.loaded()
        self.isLoading = True
        offersLoaderLabel = Label(self.frame, text="Ładowanie...", width="10")
        offersLoaderLabel.pack()

    def loaded(self):
        self.isLoading = False
        for widget in self.frame.winfo_children():
            widget.destroy()
