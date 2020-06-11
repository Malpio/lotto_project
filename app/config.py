import socket
import abc

tcp_socket = serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_config = ('127.0.0.1', 40000)
date_format = '%d/%m/%Y %H:%M:%S'
lotto_price = 5

response_codes = {
    'REGISTER_OK': 'Rejestracja powiodła się',
    'USERNAME_ALREADY_EXIST': 'Użytkownik z taką nazwą już istnieje',
    'LOGIN_OK': 'Logowanie powiodło się',
    'LOGIN_FAIL': 'Niepoprawne dane logowania',
    'BALANCE_AMOUNT': 'Ilość srodków na koncie',
    'NO_ENOUGH_BALANCE': 'Ilość środków na koncie jest niewystarczające',
    'COUPON_BUY_OK': 'Pomyślnie kupiono los',
    'COUPON_INVALID_NUMBERS': 'Ilość liczb lub ich wartości są nieprawidłowe'
}

'''COMMANDS LIST
    ELO + public_key - Nawiązanie połączenia szyfrowanego
    REGISTER - Rejestracja użytkownika
    LOGIN - Logowanie użytkownika
    BALANCE - Zarządzanie stanem konta
    UNEXPECTED_ERROR - Nieoczekiwany błąd serwera
    LAST_WON - Sprawdzanie ostatnich wygranych
    COUPON_BUY - Kupowanie losu
    MY_COUPONS - Sprawdzanie listy moich kuponów
    WON_LIST - List ostatnich wygranych
'''


class Connection:
    __metaclass__ = abc.ABCMeta

    def __init__(self, connection):
        self.connection = connection
        self.client_public_key = None

    def __del__(self):
        self.connection.close()

    def send_request(self, request):
        request = request + '\r\n'
        self.connection.sendall(request.encode())

    def get_response(self):
        response = b''
        while not b'\r\n' in response:
            data = self.connection.recv(1)
            response += data
        response = response.decode()[:-2]
        return response

    @staticmethod
    def get_command_and_params(response):
        try:
            array = response.split(' ')
            command = array[0]
            params = array[1:]
            return {'command': command, 'params': params}
        except:
            array = response.split(' ')
            command = array[0]
            return {'command': command, 'params': []}

    def define_action(self, command, params):
        lower_command = command.lower()
        if lower_command == 'elo':
            self.save_and_send_key(params)
        elif lower_command == 'register':
            self.register(params)
        elif lower_command == 'login':
            self.login(params)
        elif lower_command == 'add_balance':
            self.balance(params)
        elif lower_command == 'unexpected_error':
            self.unexpected_error(params)
        elif lower_command == 'last_won':
            self.last_won(params)
        elif lower_command == 'coupon_buy':
            self.coupon_buy(params)
        elif lower_command == 'my_coupons':
            self.my_coupons(params)

    @abc.abstractmethod
    def save_and_send_key(self, params):
        return

    @abc.abstractmethod
    def register(self, params):
        return

    @abc.abstractmethod
    def login(self, params):
        return

    @abc.abstractmethod
    def add_balance(self, params):
        return

    @abc.abstractmethod
    def last_won(self, params):
        return

    @abc.abstractmethod
    def coupon_buy(self, params):
        return

    @abc.abstractmethod
    def my_coupons(self, params):
        return

    # def sefe_connection(self, public_key, certificate):
    #     selfcontext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='server.crt')
    #     context.load_cert_chain(certfile='client.crt', keyfile='client.key')
