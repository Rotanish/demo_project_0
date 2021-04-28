#! bin/python


from flask import Flask
from pony.flask import Pony
from model import db
from no_csrf import CSRF
from login import Login
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment

test=False

wm_purse = "__"
wm_secret = "__"
wm_secret20 = "__"

password_secret = b'__'
csrf = CSRF('__')

pp_client_id = None
pp_client_secret = None
pp_environment = None

if test:
    pp_client_id = "__"
    pp_client_secret = "__"
    pp_environment = SandboxEnvironment(
        client_id=pp_client_id, client_secret=pp_client_secret)
else:
    pp_client_id = "__"
    pp_client_secret = "__"
    pp_environment = LiveEnvironment(
        client_id=pp_client_id, client_secret=pp_client_secret)

pp_client = PayPalHttpClient(pp_environment)

app = Flask("__name__", static_url_path='',
            static_folder='./static/')

app.config.update(dict(
    DEBUG=False,
    SECRET_KEY=b'__',
    PONY={
        'provider':'sqlite', 'filename':'database.sqlite', 'create_db':True
    }

))


my_login = Login(db)

Pony(app)
