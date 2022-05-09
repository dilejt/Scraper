from os import sep
import tkinter as tk
from pandastable import Table
from consts import DELIMITER, ENCODING, ROOT_DIR
from loader import Loader


class mergedCsvFrame():
    def showMergedCsvFiles(self):
        root = tk.Tk()

        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)

        pt = Table(frame, sep=DELIMITER)
        pt.show()
        pt.importCSV(filename=ROOT_DIR + "\combined_csv.csv", engine='python', sep=DELIMITER, header=None)