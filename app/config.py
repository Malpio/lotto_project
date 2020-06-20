import socket
import abc
from _thread import *
from datetime import *
import time
import ssl

# tcp_socket = serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_config = ('localhost', 40001)
date_format = '%d/%m/%Y %H:%M:%S'
lotto_price = 5
lottery_time = 2
response_codes = {
    'REGISTER_OK': 'Rejestracja powiodła się',
    'USERNAME_ALREADY_EXIST': 'Użytkownik z taką nazwą już istnieje',
    'LOGIN_OK': 'Logowanie powiodło się',
    'LOGIN_FAIL': 'Niepoprawne dane logowania',
    'BALANCE_AMOUNT': 'Ilość srodków na koncie',
    'NO_ENOUGH_BALANCE': 'Ilość środków na koncie jest niewystarczające',
    'COUPON_BUY_OK': 'Pomyślnie kupiono los',
    'COUPON_INVALID_NUMBERS': 'Ilość liczb lub ich wartości są nieprawidłowe',
    'ADD_BALANCE_OK': 'Konto zostało doładowane',
    'ADD_BALANCE_FAIL': 'Nie udało się dodać środków',
    'NO_LOGIN': 'Nie jesteś zalogowany',
    'COUPON_BUY_LOTTERY_PROBLEM': 'Problem z wyborem najnowszej loterii',
    'LOGOUT_OK': 'Wylogowano pomyślnie',
    'GET_LOTTERY_DATE_FAIL': 'Błąd podczas pobrania daty loterii'
}

'''COMMANDS LIST
    ELO + public_key - Nawiązanie połączenia szyfrowanego
    REGISTER - Rejestracja użytkownika
    LOGIN - Logowanie użytkownika
    ADD_BALANCE - Dodawanie środków na konto
    GET_BALANCE - Sprawdzanie stanu konta
    UNEXPECTED_ERROR - Nieoczekiwany błąd serwera
    LAST_WON - Sprawdzanie ostatnich wygranych
    COUPON_BUY - Kupowanie losu
    MY_COUPONS - Sprawdzanie listy moich kuponów
    WON_LIST - List ostatnich wygranych
    NO_COMMAND - Nie zdefiniowano akcji dla polecenia
    PARAMS_COUNT - Niepoprawna liczba parametrów
    NO_LOGIN - Nie jesteś zalogowany
    LOGOUT - Wylogowywanie
    GET_LOTTERY_DATE - Pobieranie daty następnej loterii
    DISCONNECT - Zakończenie połączenia
    MAIN_PRIZE - Sprawdzanie głównej nagrody 
'''


def save_logs(client, action):
    f = open("log.txt", "a")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S:%f")
    f.write(dt_string + ": " + str(client) + ": " + str(action) + "\n")
    f.close()


class Connection:
    __metaclass__ = abc.ABCMeta

    def __init__(self, connection):
        self.connection = connection
        self.client_public_key = None
        self.main_connection = True
        start_new_thread(self.get_response, ())

    def disconnect(self):
        self.main_connection = False
        self.connection.close()

    def send_request(self, request):
        save_logs(self.connection, request)
        request = request + '\r\n'
        time.sleep(0.1)
        self.connection.sendall(request.encode())

    def get_response(self):
        while self.main_connection:
            response = b''
            temp = False
            while not b'\r\n' in response:
                try:
                    data = self.connection.recv(1)
                    response += data
                except:
                    temp = True
                    break
            if not self.main_connection or temp:
                break
            response = response.decode()[:-2]
            command_and_params = Connection.get_command_and_params(response)
            print(command_and_params)
            start_new_thread(self.define_action, (command_and_params['command'], command_and_params['params']))
        del self

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
        if lower_command == 'register':
            self.register_action(params=params)
        elif lower_command == 'disconnect':
            self.disconnect_action(params=params)
        elif lower_command == 'login':
            self.login_action(params=params)
        elif lower_command == 'add_balance':
            self.add_balance_action(params=params)
        elif lower_command == 'unexpected_error':
            self.unexpected_error_action(params=params)
        elif lower_command == 'last_won':
            self.last_won_action(params=params)
        elif lower_command == 'coupon_buy':
            self.coupon_buy_action(params=params)
        elif lower_command == 'my_coupons':
            self.my_coupons_action(params=params)
        elif lower_command == 'won_list':
            self.won_list_action(params=params)
        elif lower_command == 'get_balance':
            self.get_balance_action(params=params)
        elif lower_command == 'no_login':
            self.no_login_action(params=params)
        elif lower_command == 'params_count':
            self.params_count_action(params=params)
        elif lower_command == 'logout':
            self.logout_action(params=params)
        elif lower_command == 'get_lottery_date':
            self.get_lottery_date_action(params=params)
        elif lower_command == 'main_prize':
            self.main_prize_action(params=params)
        else:
            self.no_command_action()

    @abc.abstractmethod
    def disconnect_action(self, params=None):
        return

    @abc.abstractmethod
    def register_action(self, params=None):
        return

    @abc.abstractmethod
    def login_action(self, params=None):
        return

    @abc.abstractmethod
    def add_balance_action(self, params=None):
        return

    @abc.abstractmethod
    def last_won_action(self, params=None):
        return

    @abc.abstractmethod
    def coupon_buy_action(self, params=None):
        return

    @abc.abstractmethod
    def my_coupons_action(self, params=None):
        return

    @abc.abstractmethod
    def unexpected_error_action(self, params=None):
        return

    @abc.abstractmethod
    def no_command_action(self):
        return

    @abc.abstractmethod
    def won_list_action(self, params=None):
        return

    @abc.abstractmethod
    def get_balance_action(self, params=None):
        return

    @abc.abstractmethod
    def no_login_action(self, params=None):
        return

    @abc.abstractmethod
    def params_count_action(self, params=None):
        return

    @abc.abstractmethod
    def logout_action(self, params=None):
        return

    @abc.abstractmethod
    def get_lottery_date_action(self, params=None):
        return

    @abc.abstractmethod
    def main_prize_action(self, params=None):
        return

    # def sefe_connection(self, public_key, certificate):
    #     selfcontext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='server.crt')
    #     context.load_cert_chain(certfile='client.crt', keyfile='client.key')
