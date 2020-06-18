from app.config import tcp_socket, connection_config, Connection
from app.database import Database
import ssl
import hashlib
import sqlite3
from _thread import *
import random
import time



server_socket = tcp_socket
server_socket.bind(connection_config)
server_socket.listen(5)

# d = Database()

class Connect(Connection):
    def __init__(self, client):
        Connection.__init__(self, client)
        self.userID = None

    def register_action(self, params=None):
        database = Database()
        if params and len(params) == 4:
            response = database.register(params[0], params[1], params[2], hashlib.md5(params[3].encode()).digest())
            self.send_request(response['response'])
        else:
            self.send_request('PARAMS_COUNT')
        del database

    def login_action(self, params=None):
        database = Database()
        if params and len(params) == 2:
            response = database.login(params[0], hashlib.md5(params[1].encode()).digest())
            self.send_request(response['response'])
            try:
                id = response['user_id']
                print(id)
                self.userID = int(id)
            except:
                pass
        else:
            self.send_request('PARAMS_COUNT')
        del database

    def add_balance_action(self, params=None):
        database = Database()
        response = database.add_balance(params[0], params[1])
        self.send_request(response['response'])
        del database

    def last_won_action(self, params=None):
        try:
            database = Database()
            if params and len(params) == 1:
                response = database.get_last_lotto(int(params[0]))
                self.send_request(response['response'])
            else:
                self.send_request('PARAMS_COUNT')
            del database
        except:
            self.send_request('UNEXPECTED_ERROR')

    def won_list_action(self, params=None):
        try:
            database = Database()
            response = database.get_won_list()
            self.send_request(response['response'])
            del database
        except:
            self.send_request('UNEXPECTED_ERROR')

    def coupon_buy_action(self, params=None):
        database = Database()
        response = database.buy_coupon(params[0], params[1], params[2])
        self.send_request(response['response'])
        del database

    def my_coupons_action(self, params=None):
        database = Database()
        response = database.get_user_coupons(params[0])
        for x in response:
            print(x)
        #print(response['response'])
        #self.send_request(response['response'])
        del database

    def get_balance_action(self, params=None):
        database = Database()
        if self.userID:
            response = database.get_balance(self.userID)
            self.send_request(response['response'])
        else:
            self.send_request('GET_BALANCE NO_LOGIN')


    def unexpected_error_action(self, params=None):
        self.send_request('UNEXPECTED_ERROR')

    def no_command_action(self):
        self.send_request('NO_COMMAND')




while True:
    client_connect, addr = server_socket.accept()
    client_connection = Connect(client_connect)
