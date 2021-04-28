#! bin/python


from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest, OrdersGetRequest
from flask import session, request, jsonify, redirect
from pony.orm import *
from hashlib import sha3_512 as my_hash, md5, sha256
from model import *
from helpers import *
from config import app, csrf, my_login, password_secret, \
    wm_secret20, wm_secret, wm_purse, pp_client, test


# Front
@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file("index.html")


# API
@app.route("/api/get-reviews", methods=["GET"])
def get_reviews():
    messages = []
    print(my_login.get_user(session))
    if my_login.get_user(session):
        messages_db = select(m for m in Message)
    else:
        messages_db = select(m for m in Message if m.status == 'moderated_ok')
    for message in messages_db:
        mes = message.to_dict()
        mes['time_post'] = str(mes['time_post'])[
            :str(mes['time_post']).rfind(':')]
        if message.autor:
            mes['autor'] = message.autor.to_dict(only=['nickname', 'avatar'])
        messages.append(mes)
    return jfy(list(reversed(messages)))


@app.route("/api/send-reviews", methods=["POST"])
def send_reviews():
    form = strip_form(request.get_json(True))
    if csrf.check_token(session, form['csrf']) and form['review']:
        current_user = my_login.get_user(session)
        if current_user:
            form['review']
            Message(description=form['review'], time_post=datetime.now(
            ), autor=current_user, nickname=current_user.nickname, status="moderated_ok")
        else:
            if 'nickname_hash' not in session:
                session['nickname_hash'] = md5(
                    session['CSRF_KEY'].encode()).hexdigest()
            nickname = session['nickname_hash'][:4] + \
                "-" + session['nickname_hash'][-4:]
            Message(description=form['review'], time_post=datetime.now(
            ), nickname=nickname, status="moderated")
        return jsonify({'status': "OK"})
    return jsonify({'status': "Oops"})


@app.route("/api/moderating", methods=["POST"])
def moderating():
    form = strip_form(request.get_json(True))
    if csrf.check_token(session, form['csrf']):
        current_user = my_login.get_user(session)
        if current_user:
            id = int(form['id'])
            if form['command'] == 'delete':
                Message[id].delete()
            if form['command'] == 'ok':
                Message[id].status = 'moderated_ok'
            return jsonify({'status': "OK"})
    return jsonify({'status': "Oops"})


@app.route("/api/send-thanks", methods=["POST"])
def send_thanks():
    form = strip_form(request.get_json(True))
    if csrf.check_token(session, form['csrf']):
        if 'nickname_hash' not in session:
            session['nickname_hash'] = md5(
                session['CSRF_KEY'].encode()).hexdigest()
        l = Liked.get(identificator=session['nickname_hash'])
        if l:
            l.delete()
            return jsonify({'status': "OK", 'thanks': False})
        else:
            Liked(identificator=session['nickname_hash'])
            return jsonify({'status': "OK", 'thanks': True})
    return jsonify({'status': "Oops"})


@app.route("/api/get-thanks", methods=["GET"])
def get_thanks():
    if 'nickname_hash' not in session:
        session['nickname_hash'] = md5(
            session['CSRF_KEY'].encode()).hexdigest()
    if Liked.get(identificator=session['nickname_hash']):
        return jsonify({'count': len(select(l for l in Liked)), 'thanks': True})
    else:
        return jsonify({'count': len(select(l for l in Liked)), 'thanks': False})


# PAY
def price_list():
    pl = {}
    for i in PriceList.select():
        pl[i.server] = i.koef
    return pl


@app.route("/api/get-price-list", methods=["GET"])
def get_price_list():
    return jfy(price_list())


@app.route("/api/pay-start", methods=["POST"])
def pay_start():
    form = strip_form(request.get_json(True))
    if csrf.check_token(session, form['csrf']) and validate_form(form, price_list()):
        desk = str("server- "+str(form['server']) +
                   " | gold- "+str(form['gold']) +
                   " | nickname- "+str(form['nickname']))
        if form['pay'] == 'PayPal':
            payment = Payment(
                gold=Decimal(form['gold']),
                price=Decimal(form['price']),
                server=str(form['server']),
                nickname=str(form['nickname']),
                email=str(form['email']),
                faction=str(form['faction']),
                payment="paypal",
                status="creating",
                create_time=datetime.now()
            )
            if len(desk) > 127:
                desk = desk[:126]
            pp_request = OrdersCreateRequest()
            pp_request.prefer('return=representation')
            pp_request.request_body({
                "intent": "CAPTURE",
                "application_context": {
                    "return_url": "https://boomkin-gold.com/pp-success",
                    "cancel_url": "https://boomkin-gold.com/fail",
                },
                "purchase_units": [{
                    "amount": {
                        "currency_code": "USD",
                        "value": str(Decimal(form['price']))
                    },
                    "description": desk
                }]
            })
            response = pp_client.execute(pp_request)
            if response.status_code != 201:
                return jfy({'status': 'Oops'})
            approve_link = ""
            for link in response.result.links:
                if link.rel == "approve":
                    approve_link = link.href
            if approve_link == "":
                return jfy({'status': 'Oops'})
            payment.pp_order = str(response.result.id)
            return jfy({'status': 'OK', 'payment': 'paypal', 'approveLink': approve_link})
        if form['pay'] == 'WebMoney':
            payment = Payment(
                gold=Decimal(form['gold']),
                price=Decimal(form['price']),
                server=str(form['server']),
                nickname=str(form['nickname']),
                email=str(form['email']),
                faction=str(form['faction']),
                payment="webmoney",
                status="creating",
                create_time=datetime.now()
            )
            if len(desk) > 254:
                desk = desk[:253]
            params = {}
            if test:
                params['LMI_SIM_MODE'] = "2" 
            params['LMI_PAYEE_PURSE'] = wm_purse
            params['LMI_PAYMENT_AMOUNT'] = str(Decimal(form['price']))
            params['LMI_PAYMENT_DESC'] = desk
            params['LMI_PAYMENT_NO'] = str(payment.id)
            params['LMI_PAYMER_EMAIL'] = str(form['email'])
            params['LMI_PAYMENTFORM_SIGN'] = str(sha256(";".join([params['LMI_PAYEE_PURSE'],
                                                                  params['LMI_PAYMENT_AMOUNT'],
                                                                  params['LMI_PAYMENT_NO'],
                                                                  wm_secret20,
                                                                  '']).encode()).hexdigest())

            return jfy({'status': 'OK',
                        'payment': 'webmoney',
                        'action': 'https://merchant.webmoney.ru/lmi/payment_utf.asp',
                        'params': params})
    return jfy({'status': 'Oops'})


def pp_check(token):
    pp_request = OrdersGetRequest(token)
    response = pp_client.execute(pp_request)
    try:
        pay = select(p for p in Payment if p.pp_order == token).first()
        pay.status = response.result.status
        pay.last_update_time = datetime.now()
        if response.result.status == "COMPLETED":
            return redirect('/success')
    except:
        print("error check order")
    return redirect('/fail')


@app.route("/pp-success", methods=["GET"])
def pp_success():
    token = str(request.args.get('token'))
    try:
        pp_request = OrdersCaptureRequest(token)
        pp_client.execute(pp_request)
    except:
        print("error capture... check order")
    return pp_check(token)


@app.route("/wm-result", methods=["POST"])
def wm_result():
    if not str(request.remote_addr)[:str(request.remote_addr).rfind('.')] in ["212.118.48", "91.200.28", "91.227.52"]:
        return ''
    if not request.form:
        return ''
    form = request.form
    if form.get('LMI_HASH2') == sha256(';'.join([form.get('LMI_PAYEE_PURSE'),
                                                 form.get('LMI_PAYMENT_AMOUNT'),
                                                 # form.get('LMI_HOLD'),
                                                 '',
                                                 form.get('LMI_PAYMENT_NO'),
                                                 form.get('LMI_MODE'),
                                                 form.get('LMI_SYS_INVS_NO'),
                                                 form.get('LMI_SYS_TRANS_NO'),
                                                 form.get(
                                                     'LMI_SYS_TRANS_DATE'),
                                                 wm_secret,
                                                 form.get('LMI_PAYER_PURSE'),
                                                 form.get('LMI_PAYER_WM')]).encode()).hexdigest():
        pay = select(p for p in Payment if p.id ==
                     form.get('LMI_PAYMENT_NO')).first()
        pay.status = "COMPLETED"
        pay.last_update_time = datetime.now()
        return ''


# AUTH
@app.route("/api/csrf", methods=["GET"])
def create_csrf():
    csrf.generate_key(session)
    return csrf.create_token(session)


# ADMIN
@app.route('/api/whoami', methods=["GET"])
def whoami():
    current_user = my_login.get_user(session)
    if current_user:
        return jsonify({
            'login': current_user.login,
            'nickname': current_user.nickname,
            'avatar': current_user.avatar,
            'status': "auth",
        })
    else:
        return jsonify({
            'status': "not auth",
            'login': "",
            'nickname': "",
            'avatar': "",
        })


@app.route("/api/login", methods=["POST"])
def login():
    current_user = my_login.get_user(session)
    if current_user:
        return "Already logined"
    form = strip_form(request.get_json(True))
    if csrf.check_token(session, form['csrf']) and validate_log(form):
        user = Admin.get(login=form['login'])
        if user:
            if user.password_hash == my_hash(password_secret + str(form['password']).encode() + user.password_salt.encode()).hexdigest():
                my_login.login(session, user, request.remote_addr)
                return "Logined"
        return "Wrong login or password"
    return "Oops"


@app.route('/api/logout', methods=["POST"])
def logout():
    current_user = my_login.get_user(session)
    if current_user:
        form = request.get_json(True)
        form = strip_form(form)
        if csrf.check_token(session, form['csrf']):
            my_login.logout(session)
            return "Logout"
    return "Oops"


@app.route('/api/logoutall', methods=["POST"])
def logout_all():
    current_user = my_login.get_user(session)
    if current_user:
        form = request.get_json(True)
        form = strip_form(form)
        if csrf.check_token(session, form['csrf']):
            my_login.logout_all(session)
            return "Logout"
    return "Oops"


@app.route("/api/get-sessions", methods=["GET"])
@db_session
def get_sessions():
    user = str(request.args.get('user'))
    current_user = my_login.get_user(session)
    if current_user:
        if current_user.admin_lvl > 1:  # На админа
            return dbo_to_json(select(p for p in Session if Admin.get(login=user) == p.user))
        else:
            return dbo_to_json(select(p for p in Session if Admin.get(login=current_user.login) == p.user))
    return jsonify({'status': "Oops", 'login': ''})


@app.route("/api/kill-sessions", methods=["GET"])
@db_session
def kill_session():
    identificator = str(request.args.get('identificator'))
    current_user = my_login.get_user(session)
    if current_user:
        my_login.kill_session(session, identificator)
    return jsonify({'status': "Oops", 'login': ''})
