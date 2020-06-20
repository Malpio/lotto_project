from app.config import tcp_socket, connection_config, Connection
from app.database import Database
from app.utils import Utils
import ssl
import hashlib
import sqlite3
from _thread import *
import random
import time



server_socket = tcp_socket
server_socket.bind(connection_config)
server_socket.listen(5)


class Connect(Connection):
    def __init__(self, client):
        Connection.__init__(self, client)
        self.userID = None

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

            else:
                self.send_request('PARAMS_COUNT')
            id = response['user_id']
            print(id)
            self.userID = int(id)
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

    def unexpected_error_action(self, params=None):
        self.send_request('UNEXPECTED_ERROR')

    def no_command_action(self):
        self.send_request('NO_COMMAND')




while True:
    client_connect, addr = server_socket.accept()
    client_connection = Connect(client_connect)
