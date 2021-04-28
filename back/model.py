#! bin/python


from pony.orm import *
from datetime import datetime
from decimal import Decimal

db = Database()


class Message(db.Entity):
    description = Required(str)
    time_post = Required(datetime)
    status = Required(str)
    autor = Optional('Admin', reverse='message')
    nickname = Optional(str)
    title = Optional(str)


class Admin(db.Entity):
    login = PrimaryKey(str)
    password_hash = Required(str)
    password_salt = Required(str)
    nickname = Required(str)
    session = Set('Session', reverse='user')
    reg_time = Required(datetime)
    admin_lvl = Optional(int)
    avatar = Optional(str)
    message = Set('Message', reverse='autor')


class Session(db.Entity):
    identificator = PrimaryKey(str)
    user = Required('Admin', reverse='session')
    login_time = Required(datetime)
    last_active_time = Optional(datetime)
    ip = Optional(str)


class Liked(db.Entity):
    identificator = PrimaryKey(str)


class Payment(db.Entity):
    gold = Required(Decimal)
    price = Required(Decimal)
    server = Required(str)
    nickname = Required(str)
    faction = Required(str)
    email = Required(str)
    payment = Required(str)
    status = Required(str)
    create_time = Required(datetime)
    last_update_time = Optional(datetime)
    pp_order = Optional(str)


class PriceList(db.Entity):
    server = Required(str)
    koef = Required(Decimal)
