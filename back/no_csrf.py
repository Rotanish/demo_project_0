#! bin/python


from random import randint, choice
from hashlib import sha3_256 as s_hash


class CSRF:
    def __init__(self, server_key, salt='__'):
        self.server_key = str(server_key)
        self.salt = str(salt)
        self.__all_char = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"

    def _create(self, client_key):
        client_key = str(client_key)
        rn = str(randint(100, 1000000000))
        key = str(client_key) + rn + self.server_key + self.salt
        token = rn + '$' + s_hash(key.encode()).hexdigest() + '=='
        return token

    def _verify(self, client_key, csrf_token):
        client_key = str(client_key)
        csrf_token = str(csrf_token)
        rn = csrf_token[:csrf_token.index('$')]
        key = str(client_key) + rn + self.server_key + self.salt
        client_token = rn + '$' + s_hash(key.encode()).hexdigest() + '=='

        return client_token == csrf_token

    def regenerate_key(self, session):
        session['CSRF_KEY'] = ''.join(
            choice(self.__all_char) for i in range(30))
        return True

    def generate_key(self, session):
        if 'CSRF_KEY' not in session:
            self.regenerate_key(session)
        return True

    def create_token(self, session):
        self.generate_key(session)
        return self._create(session['CSRF_KEY'])

    def check_token(self, session, csrf):
        if 'CSRF_KEY' in session:
            return self._verify(session['CSRF_KEY'], csrf)
        return None
