from tkinter import *
from app.gui.config import colors


class LottoGUI(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.is_login = False
        # self.socket = socket
        # NavigationMenu(self)

        self.title('Lotto')

        self.minsize(900, 700)

        container = Frame(self)
        container.place(relwidth=1, relheight=1)

        self.frames = {}
        self.navigation_stack = []

        for F in (LoginPage, RegisterPage, LottoBuyPage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame

        self.navigation(MainPage)

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

        login_entry = Entry(input_container)
        login_entry.grid(row=0, column=1)

        password_label = Label(input_container, text="Hasło: ", bg=colors['light_gray'])
        password_label.config(font=("Aria", 15))
        password_label.grid(row=1, column=0, pady=20)

        password_entry = Entry(input_container)
        password_entry.grid(row=1, column=1)

        login_button = Button(input_container, text="Zaloguj", bg=colors['light_gray'], command=lambda: controller.navigation(MainPage))
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

        name_entry = Entry(input_container)
        name_entry.grid(row=0, column=1, pady=5)

        last_name_label = Label(input_container, text="Nazwisko: ", bg=colors['light_gray'])
        last_name_label.config(font=("Aria", 15))
        last_name_label.grid(row=1, column=0, pady=5)

        last_name_entry = Entry(input_container)
        last_name_entry.grid(row=1, column=1, pady=5)

        login_label = Label(input_container, text="Login: ", bg=colors['light_gray'])
        login_label.config(font=("Aria", 15))
        login_label.grid(row=2, column=0, pady=5)

        login_entry = Entry(input_container)
        login_entry.grid(row=2, column=1, pady=5)

        password_label = Label(input_container, text="Hasło: ", bg=colors['light_gray'])
        password_label.config(font=("Aria", 15))
        password_label.grid(row=3, column=0, pady=5)

        password_entry = Entry(input_container)
        password_entry.grid(row=3, column=1)

        confirm_password_label = Label(input_container, text="Powtórz hasło: ", bg=colors['light_gray'])
        confirm_password_label.config(font=("Aria", 15))
        confirm_password_label.grid(row=4, column=0, pady=5)

        confirm_password_entry = Entry(input_container)
        confirm_password_entry.grid(row=4, column=1, pady=5)

        register_button = Button(input_container, text="Zarejestruj", bg=colors['light_gray'])
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

        self.navigation(LottoBuyPage)

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

        entry_1 = Entry(buy_container)
        entry_1.grid(row=1, column=0, padx=10, pady=10)
        entry_1.config(width=4)

        entry_2 = Entry(buy_container)
        entry_2.grid(row=1, column=1, padx=10, pady=10)
        entry_2.config(width=4)

        entry_3 = Entry(buy_container)
        entry_3.grid(row=1, column=2, padx=10, pady=10)
        entry_3.config(width=4)

        entry_4 = Entry(buy_container)
        entry_4.grid(row=2, column=0)
        entry_4.config(width=4)

        entry_5 = Entry(buy_container)
        entry_5.grid(row=2, column=1)
        entry_5.config(width=4)

        entry_6 = Entry(buy_container)
        entry_6.grid(row=2, column=2)
        entry_6.config(width=4)

        buy_button = Button(buy_container, text='Kup los', bg=colors['light_gray'], command=lambda: self.buy())
        buy_button.config(width=17, height=3)
        buy_button.grid(row=3, columnspan=3, pady=30)

    def buy(self):
        pass


class MyAccountPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        main_label = Label(self, text='Moje konto')
        main_label.config(font=("Aria", 20))
        main_label.pack()

        left_container = Frame(self, highlightbackground=colors['gray'], highlightthickness=1)
        left_container.place(relx=0, rely=1, relwidth=0.35, relheight=0.92, anchor=SW)

        right_container = Frame(self)
        right_container.place(relx=1, rely=1, relwidth=0.65, relheight=0.92, anchor=SE)

        balance_container = Frame(left_container)
        balance_container.place(relx=0.5, rely=0.05, relheight=0.95, anchor=N)

        balance_label = Label(balance_container, text='Stan konta: ' + str(self.get_account_balacne()) + 'zł')
        balance_label.config(font=("Aria", 14))
        balance_label.grid(row=0, columnspan=3)

        balance_add_label = Label(balance_container, text='Doładuj konto kwotą: ')
        balance_add_label.config(font=("Aria", 14))
        balance_add_label.grid(row=1, column=0)

        balance_entry = Entry(balance_container)
        balance_entry.config(width=5)
        balance_entry.grid(row=1, column=1)

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
        # return self.balance
        return 20

    def add_balance(self):
        pass


class LottoPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller

        main_label = Label(self, text='Wyniki losowań loterii Lotto')
        main_label.config(font=("Aria", 20))
        main_label.pack()


# class NavigationMenu:
#     def __init__(self, master):
#         menubar = Menu(master)
#         filemenu = Menu(menubar, tearoff=0)
#         filemenu.add_command(label="Kup los", command=lambda: master.navigation(LottoBuyPage))
#         menubar.add_cascade(label="Menu", menu=filemenu)
#
#         master.config(menu=menubar)


app = LottoGUI()
app.mainloop()

