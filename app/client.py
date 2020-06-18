from app.config import connection_config, tcp_socket, Connection, response_codes
from app.cert_creator import *
from _thread import *
import time
from app.gui.gui import LottoGUI
from OpenSSL import *
import ssl
import hashlib

class Client(Connection):
    def register(self, first_name, last_name, login, password):
        register_request = 'REGISTER ' + first_name + ' ' + last_name + ' ' + login + ' ' + password
        self.send_request(register_request)

    def login(self, login, password):
        login_request = 'LOGIN ' + login + ' ' + password
        self.send_request(login_request)

    def register_action(self, params=None, additional_action=None):
        if params:
            print(response_codes[params[0]])
        else:
            print('brak kodu odpowiedzi')

    def no_command_action(self):
        print('Błędne polecenie')


s = tcp_socket

try:
    s.connect(connection_config)
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_verify_locations(SERVER_CERT)
    # context.load_cert_chain(certfile=CERT_PATH, keyfile=KEY_PATH)
    # secure_socket = context.wrap_socket(socket, server_side=False, server_hostname=ip)
    client = Client(s)
    gui = LottoGUI(client=client)
    gui.mainloop()

except:
    print('error')

# s = tcp_socket
#
# try:
#     s.connect(connection_config)
#     client = Client(s)
#     print(client.register())
#     client.send_request('start')
#     client.main()
#     while True:
#         data = client.get_response()
#         command_and_params = Connection.get_command_and_params(data)
#         if command_and_params['command'].lower() == 'you-won':
#             client.send_request('you-lose')
#             break
#         elif command_and_params['command'].lower() == 'you-lose':
#             client.send_request('you-won')
#             break
#
#         else:
#             client.define_action(command_and_params['command'], command_and_params['params'])
#     del client
#
# except socket.error:
#     print('Error', socket.error)
