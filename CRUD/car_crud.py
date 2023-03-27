import tkinter as tk
import tkinter.messagebox as messagebox
from models import Car


def car_to_str(car):
    return f"{car.car_id} {car.make} {car.model_id} {car.year} {car.price} {car.trademark_id}"


class CarAdmin:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.car_listbox = tk.Listbox(self.master, width=40, height=20)
        self.year_entry = tk.Entry(self.master)
        self.model_id_entry = tk.Entry(self.master)
        self.make_entry = tk.Entry(self.master)
        self.price_entry = tk.Entry(self.master)
        self.trademark_id_entry = tk.Entry(self.master)
        self.car_id_entry = tk.Entry(self.master)
        self.info_label = tk.Label(self.master, font="Arial 10")
        self.init_widgets()
        self.fill_car_listbox()

    def init_widgets(self):
        tk.Label(self.master, text="Створити авто:", font="Arial 10 bold").grid(row=0, column=0)
        make_label = tk.Label(self.master, text="Марка:")
        make_label.grid(row=1, column=0)
        self.make_entry.grid(row=1, column=1)

        model_label = tk.Label(self.master, text="ID моделі авто:")
        model_label.grid(row=2, column=0)
        self.model_id_entry.grid(row=2, column=1)

        year_label = tk.Label(self.master, text="Рік:")
        year_label.grid(row=3, column=0)
        self.year_entry.grid(row=3, column=1)

        price_label = tk.Label(self.master, text="Ціна:")
        price_label.grid(row=4, column=0)
        self.price_entry.grid(row=4, column=1)

        trademark_label = tk.Label(self.master, text="ID компанії продавця:")
        trademark_label.grid(row=5, column=0)
        self.trademark_id_entry.grid(row=5, column=1)

        tk.Label(self.master, text="Отримати авто за id", font="Arial 10 bold").grid(row=6, column=0)
        tk.Label(self.master, text="ID авто:").grid(row=7, column=0)
        self.car_id_entry.grid(row=7, column=1)

        self.car_listbox.grid(row=8, column=0, columnspan=2)
        self.car_listbox.bind("<<ListboxSelect>>", self.on_select_car)

        get_button = tk.Button(self.master, text="Отримати авто", command=self.show_car_by_id)
        get_button.grid(row=7, column=2)

        add_button = tk.Button(self.master, text="Додати авто", command=self.add_car)
        add_button.grid(row=11, column=0)

        update_button = tk.Button(self.master, text="Оновити авто", command=self.update_car)
        update_button.grid(row=11, column=1)

        delete_button = tk.Button(self.master, text="Видалити авто", command=self.delete_car)
        delete_button.grid(row=11, column=2)

        clear_button = tk.Button(self.master, text="Очистити форми", command=self.clear_form)
        clear_button.grid(row=11, column=3)

        self.info_label.grid(row=10, column=1)

    def fill_car_listbox(self):
        self.car_listbox.delete(0, tk.END)
        for car in Car.select():
            self.car_listbox.insert(0, car_to_str(car))

    def show_car_by_id(self):
        car_id = self.car_id_entry.get()
        if car_id:
            car = Car.get_by_id(car_id)
            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, car.make or '')
            self.model_id_entry.delete(0, tk.END)
            self.model_id_entry.insert(0, car.model_id or '')
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, car.year or '')
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, car.price or '')
            self.trademark_id_entry.delete(0, tk.END)
            self.trademark_id_entry.insert(0, car.trademark_id or '')
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def add_car(self):
        make = self.make_entry.get()
        model_id = self.model_id_entry.get()
        year = self.year_entry.get()
        price = self.price_entry.get()
        trademark_id = self.trademark_id_entry.get()
        car = Car(car_id=None, make=make, model_id=model_id, year=year, price=price, trademark_id=trademark_id)
        if make and year and price and model_id and trademark_id:
            car.save()
            self.clear_form()
            self.info_label["text"] = "Авто успішно додане до БД"
            self.info_label["bg"] = "Green"
        elif make and year and price:
            car.model_id = None
            car.trademark_id = None
            car.save()
            self.car_listbox.insert(tk.END, car_to_str(car))
            self.clear_form()
            self.info_label["text"] = "Увага, відсутні зовнішні ключі, юудь ласка додайте їх потім при потребі"
            self.info_label["bg"] = "Yellow"
        else:
            messagebox.showerror("Error", "Як мінімум поля марки року та ціни є обовязковими")
        self.fill_car_listbox()

    def update_car(self):
        car_id = self.car_id_entry.get()
        if car_id:
            make = self.make_entry.get()
            model_id = self.model_id_entry.get()
            year = self.year_entry.get()
            price = self.price_entry.get()
            trademark_id = self.trademark_id_entry.get()
            if make and price and year:
                car = Car(make=make, model_id=model_id or None, year=year, price=price,
                          trademark_id=trademark_id or None)
                car.car_id = car_id
                index = self.car_listbox.get(0, tk.END).index(car_to_str(Car.get_by_id(car_id)))
                self.car_listbox.delete(index)
                car.save()
                self.car_listbox.insert(0, car_to_str(car))
                self.clear_form()
                self.info_label["text"] = "Авто успішно оновлене"
                self.info_label["bg"] = "Green"
            else:
                messagebox.showerror("Error", "Як мінімум поля марки року та ціни є обовязковими")
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим.")

    def delete_car(self):
        car_id = self.car_id_entry.get()
        if car_id:
            index = self.car_listbox.get(0, tk.END).index(str(car_to_str(Car.get_by_id(car_id))))
            self.car_listbox.delete(index)
            Car.delete_by_id(car_id)
            self.clear_form()
            self.info_label["text"] = "Авто успішно видалене з БД"
            self.info_label["bg"] = "Green"
        else:
            messagebox.showerror("Error", "Поле ID є обовязковим..")

    def clear_form(self):
        self.make_entry.delete(0, tk.END)
        self.model_id_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.trademark_id_entry.delete(0, tk.END)
        self.car_id_entry.delete(0, tk.END)

    def on_select_car(self, event):
        index = self.car_listbox.curselection()
        if index:
            car = self.car_listbox.get(index)
            car_id, make, model_id, year, price, trademark_id = self.parse_car(car)
            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, make)
            self.model_id_entry.delete(0, tk.END)
            self.model_id_entry.insert(0, model_id)
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, year)
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, price)
            self.trademark_id_entry.delete(0, tk.END)
            self.trademark_id_entry.insert(0, trademark_id)
            self.car_id_entry.delete(0, tk.END)
            self.car_id_entry.insert(0, car_id)

    def parse_car(self, car):
        car_id, make, model_id, year, price, trademark_id = car.split(" ")
        return car_id, make, model_id, year, price, trademark_id




