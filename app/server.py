from app.config import connection_config, Connection, lottery_time
from app.database import Database
from app.utils import Utils
import socket
from app.cert_creator import create_self_signed_cert
import ssl
import hashlib
import sqlite3
from _thread import *
import random
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(connection_config)
server_socket.listen(5)



class Game:
    def __init__(self, ):
        self.time = None

    def start_lottery(self):
        global d
        d = Database()
        idLotto = d.get_last_lottery_id()
        if not idLotto:
            d.create_lotto()
            idLotto = d.get_last_lottery_id()
        while True:
            if (time.localtime().tm_sec == 0 and time.localtime().tm_min % lottery_time == 0):
                numbers = []
                result = []
                for i in range(6):
                    x = False
                    while (x == False):
                        r = random.randint(1, 6)
                        if r not in numbers:
                            numbers.append(r)
                            result.append(str(r))
                            x = True

                d = Database()
                result.sort(key=int)
                d.create_lotto()
                d.update_lotto_after_lottery(str(idLotto), result)
                idLotto = d.get_last_lottery_id()
                del d
                time.sleep(2)


class Connect(Connection):
    def __init__(self, client):
        Connection.__init__(self, client)
        self.userID = None

    def disconnect_action(self, params=None):
        self.disconnect()

    def register_action(self, params=None):
        database = Database()
        try:
            if params and len(params) == 4:
                response = database.register(params[0], params[1], params[2], hashlib.md5(params[3].encode()).digest())
                self.send_request(response['response'])
            else:
                self.send_request('PARAMS_COUNT')
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def login_action(self, params=None):
        database = Database()
        try:
            if params and len(params) == 2:
                response = database.login(params[0], hashlib.md5(params[1].encode()).digest())
                self.send_request(response['response'])
                if response['response'] == 'LOGIN LOGIN_OK':
                    id = response['user_id']
                    self.userID = int(id)
            else:
                self.send_request('PARAMS_COUNT')

        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def add_balance_action(self, params=None):
        database = Database()
        try:
            if params and len(params) == 1:
                userID = self.userID
                if self.userID:
                    response = database.add_balance(userID, float(params[0]))
                    self.send_request(response['response'])
                else:
                    self.send_request('NO_LOGIN')
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def last_won_action(self, params=None):
        database = Database()
        try:
            if params and len(params) == 1:
                response = database.get_last_lotto(int(params[0]))
                self.send_request(response['response'])
            else:
                self.send_request('PARAMS_COUNT')
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def won_list_action(self, params=None):
        database = Database()
        try:
            response = database.get_won_list()
            self.send_request(response['response'])
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def coupon_buy_action(self, params=None):
        database = Database()
        try:
            if params and len(params) == 1:
                userID = self.userID
                if self.userID:
                    response = database.buy_coupon(userID, Utils.array_deserializer(params[0]))
                    self.send_request(response['response'])
                else:
                    self.send_request('NO_LOGIN')
            else:
                self.send_request('PARAMS_COUNT')
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def my_coupons_action(self, params=None):
        database = Database()
        try:
            userID = self.userID
            if self.userID:
                response = database.get_user_coupons_list_with_lottery(userID)
                self.send_request(response['response'])
            else:
                self.send_request('NO_LOGIN')
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def get_balance_action(self, params=None):
        database = Database()
        if self.userID:
            response = database.get_balance(self.userID)
            self.send_request(response['response'])
        else:
            self.send_request('NO_LOGIN')
        del database

    def unexpected_error_action(self, params=None):
        self.send_request('UNEXPECTED_ERROR')

    def no_command_action(self):
        self.send_request('NO_COMMAND')

    def logout_action(self, params=None):
        self.userID = None
        self.send_request('LOGOUT LOGOUT_OK')

    def get_lottery_date_action(self, params=None):
        database = Database()
        try:
            response = database.get_next_lottery_date()
            self.send_request(response['response'])
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

    def main_prize_action(self, params=None):
        database = Database()
        try:
            response = database.get_next_lottery_main_prize()
            self.send_request(response['response'])
        except:
            self.send_request('UNEXPECTED_ERROR')
        del database

g = Game()
start_new_thread(g.start_lottery, ())
SERVER_CERT = 'server.cert'
SERVER_KEY = 'server.key'
try:
    while True:
        client_connect, addr = server_socket.accept()
        connstream = ssl.wrap_socket(client_connect, server_side=True, certfile=SERVER_CERT, keyfile=SERVER_KEY)
        client_connection = Connect(connstream)
except Exception as e:
    print(e)



