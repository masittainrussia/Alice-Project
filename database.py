from pony.orm import *


db = Database()


class Items(db.Entity):
    id = PrimaryKey(int, auto=True)
    item = Optional(str)
    places = Set('Places')


class Places(db.Entity):
    id = PrimaryKey(int, auto=True)
    place = Optional(str)
    id_item = Required(Items)


db.bind(provider='sqlite', filename='Lost Items.db', create_db=True)
db.generate_mapping(create_tables=True)