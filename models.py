from peewee import *

mysql_db = MySQLDatabase('cartrademark', user='root', password='@rsen2003', host='localhost', port=3306)
pg_db = PostgresqlDatabase('cartrademarks', user='postgres', password='@rsen2003', host='localhost', port=5432)
sqlite_db = SqliteDatabase("cars.db")


class CarTrademark(Model):
    trademark_id = IntegerField(primary_key=True)
    trademark = CharField()

    class Meta:
        database = mysql_db
        table_name = 'cartrademarks'


class CarModel(Model):
    model_id = IntegerField(primary_key=True)
    model = CharField()
    car_id = IntegerField()

    class Meta:
        database = mysql_db
        table_name = 'models'


class Car(Model):
    car_id = IntegerField(primary_key=True)
    make = CharField()
    model_id = IntegerField()
    year = IntegerField()
    price = IntegerField()
    trademark_id = IntegerField()

    class Meta:
        database = mysql_db
        table_name = 'cars'


class CarTrademarkPgSQL(Model):
    trademark_id = IntegerField(primary_key=True)
    trademark = CharField()

    class Meta:
        database = pg_db
        table_name = 'cartrademarks'


class CarModelPgSQL(Model):
    model_id = IntegerField(primary_key=True)
    model = CharField()
    car_id = IntegerField()

    class Meta:
        database = pg_db
        table_name = 'models'


class CarPgSQL(Model):
    car_id = IntegerField(primary_key=True)
    make = CharField()
    model_id = IntegerField()
    year = IntegerField()
    price = IntegerField()
    trademark_id = IntegerField()

    class Meta:
        database = pg_db
        table_name = 'cars'


class CarSqlite(Model):
    car_id = IntegerField(primary_key=True)
    model = CharField()
    price = IntegerField()

    class Meta:
        database = sqlite_db
        table_name = 'cars'
