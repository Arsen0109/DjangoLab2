from tkinter import *
from CRUD import car_crud, trademark_crud, model_crud
from models import *
from peewee import MySQLDatabase, PostgresqlDatabase, SqliteDatabase


def call_car_crud():
    car_crud_interface = Tk()
    car_crud.CarAdmin(car_crud_interface)
    car_crud_interface.mainloop()


def call_trademark_crud():
    trademark_crud_interface = Tk()
    trademark_crud.TrademarkAdmin(trademark_crud_interface)
    trademark_crud_interface.mainloop()


def call_model_crud():
    model_crud_interface = Tk()
    model_crud.ModelAdmin(model_crud_interface)
    model_crud_interface.mainloop()


def transfer_data_to_postgresql():
    mysql_db = MySQLDatabase('cartrademark', user='root', password='@rsen2003', host='localhost', port=3306)
    pg_db = PostgresqlDatabase('cartrademarks', user='postgres', password='@rsen2003', host='localhost', port=5432)

    mysql_db.connect()
    pg_db.connect()

    for car_trademark in CarTrademark.select():
        new_ct = CarTrademarkPgSQL(trademark_id=car_trademark.trademark_id, trademark=car_trademark.trademark)
        CarTrademarkPgSQL.delete_by_id(new_ct.trademark_id)
        new_ct.save(force_insert=True)
        print(new_ct.trademark)

    for car in Car.select():
        new_car = CarPgSQL(car_id=car.car_id, make=car.make, model_id=None, year=car.year,
                           price=car.price, trademark_id=car.trademark_id)
        CarPgSQL.delete_by_id(car.car_id)
        new_car.save(force_insert=True)

    for model in CarModel.select():
        new_model = CarModelPgSQL(model_id=model.model_id, model=model.model, car_id=model.car_id)
        CarModelPgSQL.delete_by_id(model.model_id)
        new_model.save(force_insert=True)

    for car in CarPgSQL.select():
        car.model_id = Car.get_by_id(car.car_id).model_id
        car.save()
    mysql_db.close()
    pg_db.close()


def transfer_data_to_sqlite():
    pg_db = PostgresqlDatabase('cartrademarks', user='postgres', password='@rsen2003', host='localhost', port=5432)
    sqlite_db = SqliteDatabase("cars.db")

    pg_db.connect()
    sqlite_db.connect()
    sqlite_db.drop_tables(CarSqlite)
    CarSqlite.create_table()
    models_dict = {}
    cars_list = []
    for model in CarModelPgSQL.select():
        models_dict[model.model_id] = model.model
    for car in CarPgSQL.select().where(CarPgSQL.year >= 2018):
        cars_list.append({"car_id": car.car_id, "model": models_dict[car.model_id], "price": car.price})
    print(cars_list)
    with sqlite_db.atomic():
        query = CarSqlite.insert_many(cars_list)
        query.execute()
    for car in CarSqlite.select():
        print(f"{car.car_id} {car.model} {car.price}")
    pg_db.close()
    sqlite_db.close()


class AdminInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Car Admin")
        self.init_widgets()

    def init_widgets(self):
        car_interface_button = Button(self.master, text="Car CRUD interface", command=call_car_crud,
                                      width=20, height=3)
        car_interface_button.grid(row=0, column=0)

        trademark_interface_button = Button(self.master, text="Trademark CRUD interface", width=20, height=3,
                                            command=call_trademark_crud)
        trademark_interface_button.grid(row=1, column=0)

        model_interface_button = Button(self.master, text="Model CRUD interface", width=20, height=3,
                                        command=call_model_crud)
        model_interface_button.grid(row=2, column=0)

        transfer_db_button = Button(self.master, text="Transfer from MySQL to PostgreSQL", width=30, height=3,
                                    command=transfer_data_to_postgresql)
        transfer_db_button.grid(row=1, column=2)

        transfer_db_button = Button(self.master, text="Transfer from PostgreSQL to SQLite", width=30, height=3,
                                    command=transfer_data_to_sqlite)
        transfer_db_button.grid(row=0, column=2)


root = Tk()
admin_interface = AdminInterface(root)
root.mainloop()
