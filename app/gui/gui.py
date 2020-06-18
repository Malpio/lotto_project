from tkinter import *
from tkinter import messagebox
from app.gui.config import colors
from app.config import connection_config, tcp_socket, Connection, response_codes
from app.utils import Utils


class LottoGUI(Tk, Connection):
    def __init__(self, connection, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Connection.__init__(self, connection=connection)
        self.is_login = False

        # NavigationMenu(self)
        self.title('Lotto')

        self.minsize(1100, 900)

        container = Frame(self)
        container.place(relwidth=1, relheight=1)

        self.frames = {}
        self.navigation_stack = []

        for F in (LoginPage, RegisterPage, LottoBuyPage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame

        self.navigation(LoginPage)

    def navigation(self, context):
        if len(self.navigation_stack) >= 1:
            prev = self.navigation_stack[-1]
            prev.pack_forget()
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

    # def register(self, first_name, last_name, login, password):
    #     register_request = 'REGISTER ' + first_name + ' ' + last_name + ' ' + login + ' ' + password
    #     self.send_request(register_request)

    # def login(self, login, password):
    #     login_request = 'LOGIN ' + login + ' ' + password
    #     self.send_request(login_request)

    def register_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Rejestracja', response_codes[code])
            if params[0] == 'REGISTER_OK':
                self.navigation(LoginPage)
        else:
            print('brak kodu odpowiedzi')

    def login_action(self, params=None):
        if params:
            code = params[0].upper()
            messagebox.showinfo('Logowanie', response_codes[code])
            if params[0] == 'LOGIN_OK':
                self.navigation(MainPage)
                self.frames[MainPage].frames[LottoPage].get_last_won()
                self.frames[MainPage].frames[MyAccountPage].get_account_balacne()
        else:
            print('brak kodu odpowiedzi')

    def won_list_action(self, params=None):
        if params:
            last_won = Utils.deserializer(params[0])
            self.frames[MainPage].frames[LottoPage].set_last_won(last_won)
            self.frames[MainPage].frames[LottoPage].show_won_list()

    def no_command_action(self):
        print('Błędne polecenie')

    # def add_balance_action(self, params=None):
    #     if params:
    #         code = params[0].upper()
    #         messagebox.showinfo('Doładowywanie konta', response_codes[code])
    #         if code == 'ADD_BALANCE_OK':

    def get_balance_action(self, params=None):
        if params:
            balance = params[0]
            print(balance)
            self.frames[MainPage].frames[MyAccountPage].update_account_balance(balance)



class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        main_container = Frame(self, bg=colors['light_gray'])
        main_container.place(relx=0.5, rely=0.5, relwidth=0.65, relheight=0.55, anchor=CENTER)

        main_label = Label(main_container, text='Logowanie', bg=colors['light_gray'])
        main_label.config(font=("Aria", 20))
        main_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        input_container = Frame(main_container, bg=colors['light_gray'])
        input_container.place(relx=0.5, rely=0.55, anchor=CENTER)

        login_label = Label(input_container, text="Login: ", bg=colors['light_gray'])
        login_label.config(font=("Aria", 15))
        login_label.grid(row=0, column=0)

        self.login_entry = Entry(input_container)
        self.login_entry.grid(row=0, column=1)

        password_label = Label(input_container, text="Hasło: ", bg=colors['light_gray'])
        password_label.config(font=("Aria", 15))
        password_label.grid(row=1, column=0, pady=20)

        self.password_entry = Entry(input_container, show='*')
        self.password_entry.grid(row=1, column=1)

        login_button = Button(input_container, text="Zaloguj", bg=colors['light_gray'], command=self.login)
        login_button.config(height=2, width=15)
        login_button.grid(row=2, columnspan=2, pady=10)

        register_container = Frame(main_container, bg=colors['light_gray'])
        register_container.place(relx=0.95, rely=0.95, anchor=SE)

        register_label = Label(register_container, text="Nie masz jeszcze konta? ", bg=colors['light_gray'])
        register_label.config(font=("Aria", 15))
        register_label.grid(row=0, column=0)

        register_button = Button(register_container, text="Zarejestruj się!", bg=colors['light_gray'], command=lambda: controller.navigation(RegisterPage))
        register_button.config(height=1, width=10)
        register_button.grid(row=0, column=1)

    def login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login and password:
            login_request = 'LOGIN ' + login + ' ' + password
            self.controller.send_request(login_request)
            return

        messagebox.showinfo('Logowanie', 'Wypełnij wszystkie pola formularza')


class RegisterPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        main_container = Frame(self, bg=colors['light_gray'])
        main_container.place(relx=0.5, rely=0.5, relwidth=0.65, relheight=0.55, anchor=CENTER)

        main_label = Label(main_container, text='Rejestracja', bg=colors['light_gray'])
        main_label.config(font=("Aria", 20))
        main_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        input_container = Frame(main_container, bg=colors['light_gray'])
        input_container.place(relx=0.5, rely=0.55, anchor=CENTER)

        name_label = Label(input_container, text="Imię: ", bg=colors['light_gray'])
        name_label.config(font=("Aria", 15))
        name_label.grid(row=0, column=0, pady=5)

        self.name_entry = Entry(input_container)
        self.name_entry.grid(row=0, column=1, pady=5)

        last_name_label = Label(input_container, text="Nazwisko: ", bg=colors['light_gray'])
        last_name_label.config(font=("Aria", 15))
        last_name_label.grid(row=1, column=0, pady=5)

        self.last_name_entry = Entry(input_container)
        self.last_name_entry.grid(row=1, column=1, pady=5)

        login_label = Label(input_container, text="Login: ", bg=colors['light_gray'])
        login_label.config(font=("Aria", 15))
        login_label.grid(row=2, column=0, pady=5)

        self.login_entry = Entry(input_container)
        self.login_entry.grid(row=2, column=1, pady=5)

        password_label = Label(input_container, text="Hasło: ", bg=colors['light_gray'])
        password_label.config(font=("Aria", 15))
        password_label.grid(row=3, column=0, pady=5)

        self.password_entry = Entry(input_container, show='*')
        self.password_entry.grid(row=3, column=1)

        confirm_password_label = Label(input_container, text="Powtórz hasło: ", bg=colors['light_gray'])
        confirm_password_label.config(font=("Aria", 15))
        confirm_password_label.grid(row=4, column=0, pady=5)

        self.confirm_password_entry = Entry(input_container, show='*')
        self.confirm_password_entry.grid(row=4, column=1, pady=5)

        register_button = Button(input_container, text="Zarejestruj", bg=colors['light_gray'], command=self.register)
        register_button.config(height=2, width=15)
        register_button.grid(row=5, columnspan=2, pady=15)

        register_container = Frame(main_container, bg=colors['light_gray'])
        register_container.place(relx=0.95, rely=0.95, anchor=SE)

        register_label = Label(register_container, text="Masz już konto? ", bg=colors['light_gray'])
        register_label.config(font=("Aria", 15))
        register_label.grid(row=0, column=0)

        login_button = Button(register_container, text="Zaloguj się!", bg=colors['light_gray'], command=lambda: controller.navigation(LoginPage))
        login_button.config(height=1, width=10)
        login_button.grid(row=0, column=1)

    def register(self):
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not (login and password and confirm_password and name and last_name):
            messagebox.showinfo('Rejestracja', 'Wypełnij wszystkie pola formularza')
            return

        if password != confirm_password or not password:
            messagebox.showinfo('Rejestracja', 'Hasła nie są takie same')
            return

        register_request = 'REGISTER ' + name + ' ' + last_name + ' ' + login + ' ' + password
        self.controller.send_request(register_request)


class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        self.frames = {}
        self.navigation_stack = []

        top_container = Frame(self, bg=colors['light_gray'])
        top_container.place(relx=0, rely=0, relwidth=1, relheight=0.07)

        main_container = Frame(self, bg=colors['light_gray'])
        main_container.place(relx=0.5, rely=0.53, relwidth=0.95, relheight=0.87, anchor=CENTER)

        logout_button = Button(top_container, text='Wyloguj', bg=colors['light_gray'], command=lambda: self.logout())
        logout_button.place(relx=0.99, rely=0.5, relwidth=0.1, relheight=0.8, anchor=E)

        account_button = Button(top_container, text='Moje konto', bg=colors['light_gray'], command=lambda: self.navigation(MyAccountPage))
        account_button.place(relx=0.885, rely=0.5, relwidth=0.1, relheight=0.8, anchor=E)

        buy_button = Button(top_container, text='Wyniki Lotto', bg=colors['light_gray'], command=lambda: self.navigation(LottoPage))
        buy_button.place(relx=0.01, rely=0.5, relwidth=0.1, relheight=0.8, anchor=W)

        buy_button = Button(top_container, text='Kup los', bg=colors['light_gray'], command=lambda: self.navigation(LottoBuyPage))
        buy_button.place(relx=0.115, rely=0.5, relwidth=0.1, relheight=0.8, anchor=W)

        for F in (LottoBuyPage, MyAccountPage, LottoPage):
            frame = F(main_container, self)
            self.frames[F] = frame

        self.navigation(LottoPage)

    def logout(self):
        self.controller.reset_stack_then_navigate(LoginPage)

    def navigation(self, context):
        if len(self.navigation_stack) >= 1:
            prev = self.navigation_stack[-1]
            prev.pack_forget()
        frame = self.frames[context]
        self.navigation_stack.append(frame)
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()


class LottoBuyPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        main_label = Label(self, text='Kup los w loterii Lotto')
        main_label.config(font=("Aria", 20))
        main_label.pack()

        info_label = Label(self, text='Wprowadź 6 różnych liczb z zakresu od 1 do 49 i wciśnij przycisk „kup los”.\r\nPieniądze zostaną pobrane z konta automatycznie a Twój los pojawi się na stronie „Moje konto”\r\n wraz z informacjami o losowaniu do którego są przypisane.\r\n Więcej informacji o Wynikach najnowszych losowań znajdziesz w zakładce „Wyniki Lotto”.')
        info_label.config(font=("Aria", 14))
        info_label.place(relwidth=1, relx=0.5, rely=0.1, anchor=N)

        main_container = Frame(self, bg=colors['light_gray'])
        main_container.place(relx=0.5, rely=0.35, relwidth=0.6, relheight=0.52, anchor=N)

        buy_container = Frame(main_container, bg=colors['light_gray'])
        buy_container.place(relx=0.5, rely=0.5, anchor=CENTER)

        buy_label = Label(buy_container, text="Wprowadź numery", bg=colors['light_gray'])
        buy_label.config(font=("Aria", 18))
        buy_label.grid(columnspan=3, row=0, pady=20)

        self.entry_1 = Entry(buy_container)
        self.entry_1.grid(row=1, column=0, padx=10, pady=10)
        self.entry_1.config(width=4)

        self.entry_2 = Entry(buy_container)
        self.entry_2.grid(row=1, column=1, padx=10, pady=10)
        self.entry_2.config(width=4)

        self.entry_3 = Entry(buy_container)
        self.entry_3.grid(row=1, column=2, padx=10, pady=10)
        self.entry_3.config(width=4)

        self.entry_4 = Entry(buy_container)
        self.entry_4.grid(row=2, column=0)
        self.entry_4.config(width=4)

        self.entry_5 = Entry(buy_container)
        self.entry_5.grid(row=2, column=1)
        self.entry_5.config(width=4)

        self.entry_6 = Entry(buy_container)
        self.entry_6.grid(row=2, column=2)
        self.entry_6.config(width=4)

        buy_button = Button(buy_container, text='Kup los', bg=colors['light_gray'], command=self.buy)
        buy_button.config(width=17, height=3)
        buy_button.grid(row=3, columnspan=3, pady=30)

    def buy(self):
        values = [self.entry_1.get(), self.entry_2.get(), self.entry_3.get(), self.entry_4.get(), self.entry_5.get(), self.entry_6.get()]
        values = list(set(values))
        try:
            values.remove('')
        except:
            pass

        is_ok = True
        try:
            for el in values:
                v = int(el)
                if v < 1 or v > 49:
                    is_ok = False
                    break
        except ValueError:
            is_ok = False

        if len(values) != 6 or not is_ok:
            messagebox.showinfo('Kupno Losu', 'Musisz podać 6 różnych wartości z zakresu od od 1 od 49')



class MyAccountPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        self.balance = 0

        main_label = Label(self, text='Moje konto')
        main_label.config(font=("Aria", 20))
        main_label.pack()

        left_container = Frame(self, highlightbackground=colors['gray'], highlightthickness=1)
        left_container.place(relx=0, rely=1, relwidth=0.35, relheight=0.92, anchor=SW)

        right_container = Frame(self)
        right_container.place(relx=1, rely=1, relwidth=0.65, relheight=0.92, anchor=SE)

        balance_container = Frame(left_container)
        balance_container.place(relx=0.5, rely=0.05, relheight=0.95, anchor=N)

        self.balance_label = Label(balance_container, text='Stan konta: ' + str(self.balance) + 'zł')
        self.balance_label.config(font=("Aria", 14))
        self.balance_label.grid(row=0, columnspan=3)

        balance_add_label = Label(balance_container, text='Doładuj konto kwotą: ')
        balance_add_label.config(font=("Aria", 14))
        balance_add_label.grid(row=1, column=0)

        self.balance_entry = Entry(balance_container)
        self.balance_entry.config(width=5)
        self.balance_entry.grid(row=1, column=1)

        balance_add_label2 = Label(balance_container, text='zł')
        balance_add_label2.config(font=("Aria", 14))
        balance_add_label2.grid(row=1, column=2, pady=10)

        balance_add_button = Button(balance_container, text='Doładuj', command=lambda: self.add_balance())
        balance_add_button.config(height=2, width=10)
        balance_add_button.grid(row=2, columnspan=3, pady=15)

        results_header_label = Label(right_container, text='Moje losy')
        results_header_label.config(font=("Aria", 17))
        results_header_label.pack()

        results_container = Frame(right_container)
        results_container.place(relx=0.5, rely=0.07, relheight=0.92, anchor=N)

        headers = [
            {
                'column': 0,
                'row': 0,
                'text': 'Data zakupu',
            },
            {
                'column': 1,
                'row': 0,
                'text': 'Numery',
            },
            {
                'column': 2,
                'row': 0,
                'text': 'Wygrane numery',
            },
            {
                'column': 3,
                'row': 0,
                'text': 'Data losowania',
            }
        ]

        for el in headers:
            self.render_list_element(results_container, el['row'], el['column'], el['text'], 15, 10)

        row = 1
        for el in self.get_user_coupons():
            column = 0
            for el2 in el:
                self.render_list_element(results_container, row, column, el2, 6, 5)
                column += 1
            row += 1

    def render_list_element(self, container, row, column, text, padx=0, pady=0):
        element = Label(container, text=text)
        element.config(font=("Aria", 12), padx=padx, pady=pady)
        element.grid(row=row, column=column)

    def get_user_coupons(self):
        return [['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'],['07/06/2020 19:39:18', '2 3 12 23 21 49', '21 22 23 1 3 32', '07/06/2020 20:39:23'], ['07/06/2020 19:38:25', '2 3 12 23 21 22', '21 22 23 1 3 32', '07/06/2020 20:39:23'], ['07/06/2020 19:37:37', '2 3 12 23 21 22', '21 22 23 1 3 32', '07/06/2020 20:39:23'], ['07/06/2020 19:31:18', '2 3 12 23 21 21', '21 22 23 1 3 32', '07/06/2020 20:39:23']]

    def get_account_balacne(self):
        self.controller.controller.send_request('GET_BALANCE')

    def update_account_balance(self, balance):
        self.balance = balance
        self.balance_label.grid_forget()
        self.balance_label.grid(row=0, columnspan=3)

    def add_balance(self):
        balance = self.balance_entry.get()
        check = balance.split('.')
        if len(check) >= 2 and len(check[1]) > 2:
            messagebox.showinfo('Doładowywanie konta', 'Podaj liczbę z precyzją maksymalnie do dwóch miejsc po przecinku')
            return
        try:
            balance = float(balance)
            messagebox.showinfo('Doładowywanie konta', 'Konto zostało zasilone kwotą ' + str(balance) + ' zł')
        except ValueError:
            messagebox.showinfo('Doładowywanie konta', 'Musisz podać wartość liczbową')




class LottoPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller
        self.time_to_next_lottery = self.get_time_to_next_lottery()

        self.last_won = []

        main_label = Label(self, text='Następne losowanie za ' + self.time_to_next_lottery)
        main_label.config(font=("Aria", 20))
        main_label.pack()

        main_label = Label(self, text='Historia losowań dużego lotka')
        main_label.config(font=("Aria", 20))
        main_label.place(relx=0.5, rely=0.1, anchor=N)

        main_container = Frame(self, bg=colors['light_gray'])
        main_container.place(relx=0.5, rely=0.16, relwidth=1, relheight=0.84, anchor=N)

        self.result_container = Frame(main_container, bg=colors['light_gray'])
        self.result_container.place(relx=0.5, rely=0.02, relheight=1, anchor=N)

        headers = [
            {
                'column': 0,
                'row': 0,
                'text': 'Data losowania',
            },
            {
                'column': 1,
                'row': 0,
                'text': 'Główna nagroda',
            },
            {
                'column': 2,
                'row': 0,
                'text': 'Wygrane numery',
            },
            {
                'column': 3,
                'row': 0,
                'text': 'Ilość trójek',
            },
            {
                'column': 4,
                'row': 0,
                'text': 'Ilość czwórek',
            },
            {
                'column': 5,
                'row': 0,
                'text': 'Ilość piątek',
            },
            {
                'column': 6,
                'row': 0,
                'text': 'Ilość szóstek',
            }
        ]

        for el in headers:
            self.render_list_element(self.result_container, el['row'], el['column'], el['text'], 26, 15, colors['gray'])

        self.show_won_list()

        # row = 1
        # for el in self.last_won:
        #     column = 0
        #     for el2 in el:
        #         self.render_list_element(result_container, row, column, el2, 6, 5, colors['light_gray'])
        #         column += 1
        #     row += 1

    def show_won_list(self):
        self.result_container.pack_forget()
        row = 1
        for el in self.last_won:
            column = 0
            for el2 in el:
                self.render_list_element(self.result_container, row, column, el2, 6, 5, colors['light_gray'])
                column += 1
            row += 1

    def set_last_won(self, last_won):
        self.last_won = last_won

    def get_last_won(self):
        self.controller.controller.send_request('WON_LIST')
        # return [['07/06/2020 21:08:24', 'None', '21 22 23 1 3 32', '0', '0', '0', '0'], ['07/06/2020 21:08:20', 'None', '21 22 23 1 3 32', '0', '0', '0', '0'], ['07/06/2020 21:08:09', 'None', '21 22 23 1 3 32', '0', '0', '0', '0'], ['07/06/2020 20:39:23', 'None', '21 22 23 1 3 32', '2', '2', '0', '0']]

    def get_time_to_next_lottery(self):
        return '5 min'

    def render_list_element(self, container, row, column, text, padx=0, pady=0, bg=None):
        element = Label(container, text=text, bg=bg)
        element.config(font=("Aria", 11), padx=padx, pady=pady)
        element.grid(row=row, column=column)


# class NavigationMenu:
#     def __init__(self, master):
#         menubar = Menu(master)
#         filemenu = Menu(menubar, tearoff=0)
#         filemenu.add_command(label="Kup los", command=lambda: master.navigation(LottoBuyPage))
#         menubar.add_cascade(label="Menu", menu=filemenu)
#
#         master.config(menu=menubar)


s = tcp_socket
s.connect(connection_config)

app = LottoGUI(connection=s)
app.mainloop()

