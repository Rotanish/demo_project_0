#! bin/python


from pony.orm import *
from model import *
from helpers import *
from config import *
from routes import my_hash, password_secret, md5
from os import urandom

db.bind(**app.config['PONY'])


db.generate_mapping(create_tables=True)

db.drop_all_tables(with_all_data=True)

db.create_tables()


@db_session
def test_add():
    s = md5(urandom(25)).hexdigest()
    Admin(login='default',
          password_hash=my_hash(
              password_secret + "default".encode() + s.encode()).hexdigest(),
          password_salt=s,
          admin_lvl=10,
          avatar="admin.png",
          nickname='ADMIN',
          reg_time=datetime.now()
          )
    Admin(login='1',
          password_hash=my_hash(
              password_secret + "1".encode() + s.encode()).hexdigest(),
          password_salt=s,
          admin_lvl=10,
          avatar="admin.png",
          nickname='ADMIN',
          reg_time=datetime.now()
          )
    for i in [['1', 1]]:
        PriceList(server=i[0], koef=i[1])
    flush()


if __name__ == '__main__':

    test_add()

    with db_session:

        print("\n\nAdmin")
        Admin.select().show()
        print("\n\nMessage")
        Message.select().show()
        print("\n\nSession")
        Session.select().show()
        print("\n\nPayment")
        Payment.select().show()
        print("\n\nPriceList")
        PriceList.select().show()
