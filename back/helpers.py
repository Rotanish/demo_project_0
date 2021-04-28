#! bin/python


import json
from collections.abc import Iterable
from flask import jsonify
from decimal import Decimal


def jfy(obj):
    return jsonify(json.loads(json.dumps(obj, default=str)))


def dbo_to_json(dbo, metod="only", exclude='', only=[]):
    related_objects = False
    with_collections = False
    if metod == "all":
        related_objects = True
        with_collections = True
    if isinstance(dbo, Iterable):
        if only:
            return json.dumps([i.to_dict(related_objects=related_objects, with_collections=with_collections, only=only) for i in dbo], default=str)
        return json.dumps([i.to_dict(related_objects=related_objects, with_collections=with_collections, exclude=exclude) for i in dbo], default=str)
    elif type(dbo) == None or not dbo:
        print("{}")
        return json.dumps({})
    else:
        if only:
            return json.dumps(dbo.to_dict(related_objects=related_objects, with_collections=with_collections, only=only), default=str)
        return json.dumps(dbo.to_dict(related_objects=related_objects, with_collections=with_collections, exclude=exclude), default=str)


def strip_form(form):
    s_form = {}
    for key in form:
        if type(key) is str:
            s_key = key.strip()
        else:
            s_key = key
        if type(form[key]) is str:
            s_val = form[key].strip()
        else:
            s_val = form[key]
        s_form[s_key] = s_val
    return s_form


def validate_form(form, price_list):
    valid = {
        'gold': lambda put: Decimal(put) > 0,
        'price': lambda put: Decimal(put) >= 2,
        'email': lambda put: type(put) is str and len(put) <= 50 and len(put) >= 5 and '@' in put,
        'server': lambda put: type(put) is str and put in price_list,
        'nickname': lambda put: type(put) is str and len(put) <= 50 and len(put) >= 1,
        'pay': lambda put: type(put) is str and (put == "PayPal" or put == "WebMoney"),
        'faction': lambda put: str(put) in ['Alliance', 'Horde']
    }
    for key in valid:
        if not key in form:
            return False
        if not valid[key](form[key]):
            return False
    if abs(Decimal(form['gold'])-Decimal(form['price'])*Decimal(price_list[form['server']])) > Decimal(price_list[form['server']])/100:
        print("|" + str(Decimal(form['gold']))+" - "+str(Decimal(form['price']))+" * "+str(Decimal(price_list[form['server']]))+"|="+str(
            abs(Decimal(form['gold'])-Decimal(form['price'])*Decimal(price_list[form['server']])))+">"+str(Decimal(price_list[form['server']])/100))
        return False
    return True


def validate_log(form):
    valid = {
        'login': lambda put: type(put) is str and len(put) <= 25 and len(put) >= 1 and " " not in put,
        'password': lambda put: type(put) is str and len(put) <= 50 and len(put) >= 1
    }
    for key in valid:
        if not key in form:
            return False
        if not valid[key](form[key]):
            return False
    return True
