from app.config import tcp_socket, connection_config, Connection
from app.database import Database
import ssl
import hashlib
import sqlite3

server_socket = tcp_socket
server_socket.bind(connection_config)
server_socket.listen(5)

d = Database()

class Connect(Connection):
    def __init__(self):
        self.connection = sqlite3.connect('lotto.db')

    def register(self, params):
        response = d.register(params[0], params[1], params[2], hashlib.md5(params[3].encode()))
        self.send_request(response['response'])

    def login(self, params):
        response = d.login(params[0], params[1])
        self.send_request(response['response'])

    def add_balance(self, params):
        response = d.add_balance(params[0], params[1])
        self.send_request(response['response'])

    def last_won(self, params):
        response = d.get_last_lotto(params[0])
        self.send_request(response['response'])

    def coupon_buy(self, params):
        response = d.buy_coupon(params[0], params[1], params[2])
        self.send_request(response['response'])

    def my_coupons(self, params):
        print(self)
        response = d.get_user_coupons(params[0])
        for x in response:
            print(x)
        #print(response['response'])
        #self.send_request(response['response'])


c = Connect()
c.my_coupons("3")
# def create_ssl_context():
#     context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#     context.verify_mode = ssl.CERT_REQUIRED
#     context.load_cert_chain(certfile='server.crt', keyfile='server.key')
#     context.load_verify_locations(cafile='client.crt')
#     return context
#
#
# while True:
#     client, addr = server_socket.accept()
#     client_connection = Connect(client)
#     while True:
#         data = client_connection.get_response()
#         command_and_params = Connection.get_command_and_params(data)
#         if command_and_params['command'].lower() == 'you-won':
#             client_connection.send_request('you-lose')
#             break
#         elif command_and_params['command'].lower() == 'you-lose':
#             client_connection.send_request('you-won')
#             break
#         else:
#             client_connection.define_action(command_and_params['command'], command_and_params['params'])
#     del client_connection
