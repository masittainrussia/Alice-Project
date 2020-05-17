import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Item(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'item'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    item = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    places = relationship("Place", back_populates='item')


class Place(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'place'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    place = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    item_id = sqlalchemy.Column(Integer, ForeignKey('item.id'))
    item = relationship("Item", back_populates='places')

