from app.config import tcp_socket, connection_config, Connection
import ssl

server_socket = tcp_socket
server_socket.bind(connection_config)
server_socket.listen(5)


class Connect(Connection):
    pass

def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    context.load_verify_locations(cafile='client.crt')
    return context

while True:
    client, addr = server_socket.accept()
    client_connection = Connect(client)
    while True:
        data = client_connection.get_response()
        command_and_params = Connection.get_command_and_params(data)
        if command_and_params['command'].lower() == 'you-won':
            client_connection.send_request('you-lose')
            break
        elif command_and_params['command'].lower() == 'you-lose':
            client_connection.send_request('you-won')
            break
        else:
            client_connection.define_action(command_and_params['command'], command_and_params['params'])
    del client_connection
