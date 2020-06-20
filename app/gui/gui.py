from tkinter import *
from tkinter import messagebox
from app.config import connection_config, Connection, response_codes
from app.utils import Utils
from app.gui.pages.LoginPage import LoginPage
from app.gui.pages.RegisterPage import RegisterPage
from app.gui.pages.MainPage import MainPage
from app.gui.pages.MyAccountPage import MyAccountPage
from app.gui.pages.LottoPage import LottoPage
from _thread import *
import socket
import ssl
import time


class LottoGUI(Tk, Connection):
    def __init__(self, connection, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Connection.__init__(self, connection=connection)
        self.is_login = False

        self.title('Lotto')
        self.minsize(1100, 900)

        container = Frame(self)
        container.place(relwidth=1, relheight=1)

        self.frames = {}
        self.navigation_stack = []

        for F in (LoginPage, RegisterPage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame

        self.set_first_page(LoginPage)

    def on_closing(self):
        self.send_request('DISCONNECT')
        self.main_connection = False
        time.sleep(1)
        self.destroy()

    def navigation(self, context):
        if len(self.navigation_stack) >= 1:
            prev = self.navigation_stack[-1]
            prev.pack_forget()
        frame = self.frames[context]
        context.reset(frame)
        self.navigation_stack.append(frame)
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()

    def navigation_to_login(self):
        self.navigation(LoginPage)

    def navigation_to_register(self):
        self.navigation(RegisterPage)

    def set_first_page(self, context):
        frame = self.frames[context]
        self.navigation_stack.append(frame)
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()

    def reset_stack_then_navigate(self, context):
        self.navigation_stack = []
        self.navigation(context)

    def go_back(self):
        if len(self.navigation_stack) >= 2:
            prev = self.navigation_stack[-1]
            prev.pack_forget()
            self.navigation_stack.pop()
            frame = self.navigation_stack[-1]
            frame.place(relwidth=1, relheight=1)
            frame.tkraise()

    def no_login_action(self, params=None):
        messagebox.showinfo('Błąd', 'Nie jesteś zalogowany!')
        self.navigation(LoginPage)
        exit_thread()

    def unexpected_error_action(self, params=None):
        messagebox.showinfo('Błąd', 'Wystąpił nieoczekiwany błąd serwera')

    def register_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Rejestracja', response_codes[code])
            if params[0] == 'REGISTER_OK':
                self.navigation(LoginPage)

    def login_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Logowanie', response_codes[code])
            if params[0] == 'LOGIN_OK':
                self.navigation(MainPage)
                self.frames[MainPage].frames[LottoPage].get_last_won()
                self.frames[MainPage].frames[MyAccountPage].get_account_balacne()
                self.frames[MainPage].frames[MyAccountPage].get_user_coupons()
                self.frames[MainPage].frames[LottoPage].get_time_to_next_lottery()

    def won_list_action(self, params=None):
        if params:
            last_won = Utils.deserializer(params[0])
            self.frames[MainPage].frames[LottoPage].show_won_list(last_won)

    def no_command_action(self):
        messagebox.showinfo('Błąd', 'Błąd klienta - wysłano niepoprawne polecenie')

    def get_balance_action(self, params=None):
        if params:
            balance = params[0]
            self.frames[MainPage].frames[MyAccountPage].render_account_balance(balance)

    def add_balance_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Doładowywanie konta', response_codes[code])
            if code == 'ADD_BALANCE_OK':
                balance = params[1]
                self.frames[MainPage].frames[MyAccountPage].render_account_balance(balance)

    def my_coupons_action(self, params=None):
        if params:
            coupons = Utils.deserializer(params[0])
            self.frames[MainPage].frames[MyAccountPage].render_coupons(coupons)

    def coupon_buy_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Kupno losu', response_codes[code])

    def params_count_action(self, params=None):
        messagebox.showinfo('Błąd', 'Błąd klienta - niepoprawna ilość parametrów')

    def logout_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Wylogowywanie', response_codes[code])
            if code == 'LOGOUT_OK':
                self.reset_stack_then_navigate(LoginPage)

    def get_lottery_date_action(self, params=None):
        if params:
            self.frames[MainPage].frames[LottoPage].render_lottery_date(params[0])



CLIENT_CERT = 'client.cert'
CLIENT_KEY = 'client.key'

SERVER_CERT = 'server.cert'
SERVER_KEY = 'server.key'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(connection_config)
    print(SERVER_KEY, CLIENT_CERT, CLIENT_KEY)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(SERVER_CERT)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    secure_socket = context.wrap_socket(s, server_side=False, server_hostname='localhost')
    app = LottoGUI(connection=secure_socket)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
except socket.error:
    s.close()
    messagebox.showinfo('Błąd serwera', 'Nie udało się nawiązać połączenia z serwerem')
