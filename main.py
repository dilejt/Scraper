from tkinter import *
from tkinter.ttk import Treeview


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

        offers_label = Label(self.root, text="Oferty")
        offers_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        filter_frame = Frame(self.root)

        files_btn = Button(filter_frame, text="Filtruj")
        files_btn.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        office_name = Entry(filter_frame, width=40)
        office_name.grid(column=1, row=0, sticky=W, padx=5, pady=5)

        offer_type = Entry(filter_frame, width=40)
        offer_type.grid(column=2, row=0, sticky=W, padx=5, pady=5)

        price = Entry(filter_frame, width=40)
        price.grid(column=3, row=0, sticky=W, padx=5, pady=5)

        area = Entry(filter_frame, width=40)
        area.grid(column=4, row=0, sticky=W, padx=5, pady=5)

        location = Entry(filter_frame, width=40)
        location.grid(column=5, row=0, sticky=W, padx=5, pady=5)

        filter_frame.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        offers_table = Treeview(self.root)
        offers_table['columns'] = ('id', 'nazwa_biura', 'typ', 'cena', 'powierzchnia', 'lokalizacja')
        offers_table.column("#0", width=0, stretch=NO)
        offers_table.column("id", anchor=CENTER, width=80)
        offers_table.column("nazwa_biura", anchor=CENTER, width=80)
        offers_table.column("typ", anchor=CENTER, width=80)
        offers_table.column("cena", anchor=CENTER, width=80)
        offers_table.column("powierzchnia", anchor=CENTER, width=80)
        offers_table.column("lokalizacja", anchor=CENTER, width=80)
        offers_table.heading("#0", text="", anchor=CENTER)
        offers_table.heading("id", text="id", anchor=CENTER)
        offers_table.heading("nazwa_biura", text="nazwa_biura", anchor=CENTER)
        offers_table.heading("typ", text="typ", anchor=CENTER)
        offers_table.heading("cena", text="cena", anchor=CENTER)
        offers_table.heading("powierzchnia", text="powierzchnia", anchor=CENTER)
        offers_table.heading("lokalizacja", text="lokalizacja", anchor=CENTER)
        offers_table.insert(parent='', index='end', iid=0, text='',
                            values=('1', 'Ninja', '101', 'Oklahoma', 'Moore'))
        offers_table.insert(parent='', index='end', iid=1, text='',
                            values=('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'))
        offers_table.insert(parent='', index='end', iid=2, text='',
                            values=('3', 'Deamon', '103', 'California', 'Placentia'))
        offers_table.grid(column=0, row=2, sticky=W, padx=5, pady=5)

        updates_label = Label(self.root, text="Aktualności")
        updates_label.grid(column=1, row=0, sticky=W, padx=5, pady=5)

        updates_table = Treeview(self.root)
        updates_table['columns'] = ('id', 'nazwa_biura', 'typ', 'cena', 'powierzchnia', 'lokalizacja')
        updates_table.column("#0", width=0, stretch=NO)
        updates_table.column("id", anchor=CENTER, width=80)
        updates_table.column("nazwa_biura", anchor=CENTER, width=80)
        updates_table.column("typ", anchor=CENTER, width=80)
        updates_table.column("cena", anchor=CENTER, width=80)
        updates_table.column("powierzchnia", anchor=CENTER, width=80)
        updates_table.column("lokalizacja", anchor=CENTER, width=80)
        updates_table.heading("#0", text="", anchor=CENTER)
        updates_table.heading("id", text="id", anchor=CENTER)
        updates_table.heading("nazwa_biura", text="nazwa_biura", anchor=CENTER)
        updates_table.heading("typ", text="typ", anchor=CENTER)
        updates_table.heading("cena", text="cena", anchor=CENTER)
        updates_table.heading("powierzchnia", text="powierzchnia", anchor=CENTER)
        updates_table.heading("lokalizacja", text="lokalizacja", anchor=CENTER)
        updates_table.insert(parent='', index='end', iid=0, text='',
                             values=('1', 'Ninja', '101', 'Oklahoma', 'Moore'))
        updates_table.insert(parent='', index='end', iid=1, text='',
                             values=('2', 'Ranger', '102', 'Wisconsin', 'Green Bay'))
        updates_table.insert(parent='', index='end', iid=2, text='',
                             values=('3', 'Deamon', '103', 'California', 'Placentia'))
        updates_table.grid(column=1, row=2, sticky=W, padx=5, pady=5)

        button_frame = Frame(self.root)

        generate_btn = Button(button_frame, text="Generuj", width=10)
        generate_btn.grid(column=0, row=0, sticky=N, padx=5, pady=5)

        merge_btn = Button(button_frame, text="Łączenie", width=10)
        merge_btn.grid(column=0, row=1, sticky=N, padx=5, pady=5)

        files_btn = Button(button_frame, text="Pliki...", width=10)
        files_btn.grid(column=0, row=2, sticky=N, padx=5, pady=5)

        variable = StringVar(button_frame)
        variable.set("one")  # default value
        option_menu = OptionMenu(button_frame, variable, "one", "two", "three")
        option_menu.config(width=7)
        option_menu.grid(column=0, row=3, sticky=N, padx=5, pady=5)

        button_frame.grid(column=2, row=2, sticky=N, padx=5, pady=5)


if __name__ == '__main__':
    MainFrame()
