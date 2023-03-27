import tkinter as tk
import tkinter.messagebox as messagebox
from models import CarModel


def model_to_str(model):
    return f"{model.model_id} {model.model} {model.car_id}"


class ModelAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Model admin")
        self.model_listbox = tk.Listbox(self.master, width=40, height=20)
        self.model_entry = tk.Entry(self.master)
        self.car_id_entry = tk.Entry(self.master)
        self.model_id_entry = tk.Entry(self.master)
        self.info_label = tk.Label(self.master, font="Arial 10")
        self.init_widgets()
        self.fill_model_listbox()

    def init_widgets(self):
        tk.Label(self.master, text="Адмінка для Моделей авто:", font="Arial 10 bold").grid(row=0, column=0)

        tk.Label(self.master, text="Модель").grid(row=1, column=0)
        self.model_entry.grid(row=1, column=1)

        tk.Label(self.master, text="ID авто").grid(row=2, column=0)
        self.car_id_entry.grid(row=2, column=1)

        tk.Label(self.master, text="ID моделі").grid(row=3, column=0)
        self.model_id_entry.grid(row=3, column=1)

        self.model_listbox.grid(row=4, column=0, columnspan=2)
        self.model_listbox.bind("<<ListboxSelect>>", self.on_select_model)

        get_button = tk.Button(self.master, text="Отримати модель", command=self.show_model_by_id)
        get_button.grid(row=3, column=2)

        add_button = tk.Button(self.master, text="Додати модель", command=self.add_model)
        add_button.grid(row=7, column=0)

        update_button = tk.Button(self.master, text="Оновити модель", command=self.update_model)
        update_button.grid(row=7, column=1)

        delete_button = tk.Button(self.master, text="Видалити модель", command=self.delete_model)
        delete_button.grid(row=7, column=2)

        clear_button = tk.Button(self.master, text="Очистити форми", command=self.clear_form)
        clear_button.grid(row=7, column=3)

        self.info_label.grid(row=6, column=1)

    def fill_model_listbox(self):
        self.model_listbox.delete(0, tk.END)
        for model in CarModel.select():
            self.model_listbox.insert(0, model_to_str(model))

    def show_model_by_id(self):
        model_id = self.model_id_entry.get()
        if model_id:
            model = CarModel.get_by_id(model_id)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, model.model)
            self.car_id_entry.delete(0, tk.END)
            self.car_id_entry.insert(0, model.car_id)
            self.model_id_entry.delete(0, tk.END)
            self.model_id_entry.insert(0, model.model_id)
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def add_model(self):
        model_name = self.model_entry.get()
        car_id = self.car_id_entry.get()
        model = CarModel(model_id=None, model=model_name, car_id=car_id or None)
        if model_name and car_id:
            model.save()
            self.clear_form()
            self.info_label["text"] = "Модель успішно додана до БД"
            self.info_label["bg"] = "Green"
        elif model_name:
            model.save()
            self.clear_form()
            self.info_label["text"] = "Увага додана модель без зовнішніх ключів, будь ласка оновіть її пізніше."
            self.info_label["bg"] = "Yellow"
        else:
            messagebox.showerror("Error", "Як мінімум поле Модель є обовязковим.")
        self.fill_model_listbox()

    def update_model(self):
        model_id = self.model_id_entry.get()
        if model_id:
            model_name = self.model_entry.get()
            car_id = self.car_id_entry.get() or None
            if model_name:
                model = CarModel(model=model_name, car_id=car_id)
                model.model_id = model_id
                index = self.model_listbox.get(0, tk.END).index(model_to_str(CarModel.get_by_id(model_id)))
                self.model_listbox.delete(index)
                model.save()
                self.model_listbox.insert(0, model_to_str(model))
                self.clear_form()
                self.info_label["text"] = "Модель успішно оновлена."
                self.info_label["bg"] = "Green"
            else:
                messagebox.showerror("Error", "Як мінімум поле Модель є обовязковим.")
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def delete_model(self):
        model_id = self.model_id_entry.get()
        if model_id:
            index = self.model_listbox.get(0, tk.END).index(model_to_str(CarModel.get_by_id(model_id)))
            self.model_listbox.delete(index)
            CarModel.delete_by_id(model_id)
            self.clear_form()
            self.info_label["text"] = "Модель успішно видалена з БД"
            self.info_label["bg"] = "Green"
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def clear_form(self):
        self.model_entry.delete(0, tk.END)
        self.car_id_entry.delete(0, tk.END)
        self.model_id_entry.delete(0, tk.END)

    def on_select_model(self, event):
        index = self.model_listbox.curselection()
        if index: 
            model = self.model_listbox.get(index)
            model_id, model_name, car_id = self.parse_model(model)
            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, model_name)
            self.car_id_entry.delete(0, tk.END)
            self.car_id_entry.insert(0, car_id)
            self.model_id_entry.delete(0, tk.END)
            self.model_id_entry.insert(0, model_id)

    def parse_model(self, trademark):
        model_id, model_name, car_id = trademark.split(" ")
        return model_id, model_name, car_id


