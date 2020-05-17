from data import db_session
from data.models import Item, Place

db_session.global_init("base.sqlite")
session = db_session.create_session()


for i in session.query(Item):
    print(i.item)
    for j in  i.places:
        print(j.place)
