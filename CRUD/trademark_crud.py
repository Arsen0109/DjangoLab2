import tkinter as tk
import tkinter.messagebox as messagebox
from models import CarTrademark


def trademark_to_str(trademark):
    return f"{trademark.trademark_id} {trademark.trademark}"


class TrademarkAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.trademark_listbox = tk.Listbox(self.master, width=40, height=20)
        self.trademark_entry = tk.Entry(self.master)
        self.trademark_id_entry = tk.Entry(self.master)
        self.info_label = tk.Label(self.master, font="Arial 10")
        self.init_widgets()
        self.fill_trademark_listbox()

    def init_widgets(self):
        tk.Label(self.master, text="Trademark CRUD:", font="Arial 10 bold").grid(row=0, column=0)

        tk.Label(self.master, text="Trademark").grid(row=1, column=0)
        self.trademark_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Trademark_ID").grid(row=2, column=0)
        self.trademark_id_entry.grid(row=2, column=1)

        self.trademark_listbox.grid(row=3, column=0, columnspan=2)
        self.trademark_listbox.bind("<<ListboxSelect>>", self.on_select_trademark)

        get_button = tk.Button(self.master, text="Get trademark", command=self.show_trademark_by_id)
        get_button.grid(row=2, column=2)

        add_button = tk.Button(self.master, text="Add", command=self.add_trademark)
        add_button.grid(row=6, column=0)

        update_button = tk.Button(self.master, text="Update", command=self.update_trademark)
        update_button.grid(row=6, column=1)

        delete_button = tk.Button(self.master, text="Delete", command=self.delete_trademark)
        delete_button.grid(row=6, column=2)

        clear_button = tk.Button(self.master, text="Clear", command=self.clear_form)
        clear_button.grid(row=6, column=3)

        self.info_label.grid(row=5, column=1)

    def fill_trademark_listbox(self):
        self.trademark_listbox.delete(0, tk.END)
        for trademark in CarTrademark.select():
            self.trademark_listbox.insert(0, trademark_to_str(trademark))

    def show_trademark_by_id(self):
        trademark_id = self.trademark_id_entry.get()
        if trademark_id:
            trademark = CarTrademark.get_by_id(trademark_id)
            self.trademark_entry.delete(0, tk.END)
            self.trademark_entry.insert(0, trademark.trademark)
            self.trademark_id_entry.delete(0, tk.END)
            self.trademark_id_entry.insert(0, trademark.trademark_id)
        else:
            messagebox.showerror("Error", "Field car_id is empty.")

    def add_trademark(self):
        car_trademark = self.trademark_entry.get()
        trademark = CarTrademark(trademark_id=None, trademark=car_trademark)
        if car_trademark:
            trademark.save()
            self.clear_form()
            self.info_label["text"] = "Trademark successfully added to database"
            self.info_label["fg"] = "Green"
        else:
            messagebox.showerror("Error", "Field trademark is required.")
        self.fill_trademark_listbox()

    def update_trademark(self):
        trademark_id = self.trademark_id_entry.get()
        if trademark_id:
            car_trademark = self.trademark_entry.get()
            if car_trademark:
                trademark = CarTrademark(trademark=car_trademark)
                trademark.trademark_id = trademark_id
                index = self.trademark_listbox.get(0, tk.END)\
                    .index(trademark_to_str(CarTrademark.get_by_id(trademark_id)))
                self.trademark_listbox.delete(index)
                trademark.save()
                self.trademark_listbox.insert(0, trademark_to_str(trademark))
                self.clear_form()
                self.info_label["text"] = "Trademark successfully updated"
                self.info_label["fg"] = "Green"
            else:
                messagebox.showerror("Error", "At least trademark field is required.")
        else:
            messagebox.showerror("Error", "Field car_id is required.")

    def delete_trademark(self):
        trademark_id = self.trademark_id_entry.get()
        if trademark_id:
            index = self.trademark_listbox.get(0, tk.END).index(trademark_to_str(CarTrademark.get_by_id(trademark_id)))
            self.trademark_listbox.delete(index)
            CarTrademark.delete_by_id(trademark_id)
            self.clear_form()
            self.info_label["text"] = "Car successfully deleted from database"
            self.info_label["fg"] = "Green"
        else:
            messagebox.showerror("Error", "Please select a trademark to delete.")

    def clear_form(self):
        self.trademark_entry.delete(0, tk.END)
        self.trademark_id_entry.delete(0, tk.END)

    def on_select_trademark(self, event):
        index = self.trademark_listbox.curselection()
        if index:
            trademark = self.trademark_listbox.get(index)
            trademark_id, car_trademark = self.parse_trademark(trademark)
            self.trademark_entry.delete(0, tk.END)
            self.trademark_entry.insert(0, car_trademark)
            self.trademark_id_entry.delete(0, tk.END)
            self.trademark_id_entry.insert(0, trademark_id)

    def parse_trademark(self, trademark):
        trademark_id, car_trademark = trademark.split(" ")
        return trademark_id, car_trademark
