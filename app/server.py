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

d = Database()

class Connect(Connection):
    def register_action(self, params=None):
        response = d.register(params[0], params[1], params[2], hashlib.md5(params[3].encode()))
        self.send_request(response['response'])

    def login_action(self, params=None):
        response = d.login(params[0], params[1])
        self.send_request(response['response'])

    def add_balance_action(self, params=None):
        response = d.add_balance(params[0], params[1])
        self.send_request(response['response'])

    def last_won_action(self, params=None):
        response = d.get_last_lotto(params[0])
        self.send_request(response['response'])

    def coupon_buy_action(self, params=None):
        response = d.buy_coupon(params[0], params[1], params[2])
        self.send_request(response['response'])

    def my_coupons_action(self, params=None):
        print(self)
        response = d.get_user_coupons(params[0])
        for x in response:
            print(x)
        #print(response['response'])
        #self.send_request(response['response'])

    def unexpected_error_action(self, params=None):
        self.send_request('UNEXPECTED_ERROR')


while True:
    client, addr = server_socket.accept()
    client_connection = Connect(client)
