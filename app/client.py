from app.config import connection_config, tcp_socket, Connection, response_codes
import socket



class Client(Connection):
    def save_and_send_key(self, params):
        return 'qweqweqwe'

    def register(self, params):
        return 'elo'




# s = tcp_socket
#
# try:
#     s.connect(connection_config)
#     client = Client(s)
#     client.send_request('start')
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
#     print ('Error', socket.error)
