from tkinter import *
from tkinter import messagebox
from app.gui.config import colors


class MyAccountPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller
        self.balance_label = Label(self, text='Stan konta: 0 zł')
        self.list = []

        main_label = Label(self, text='Moje konto')
        main_label.config(font=("Aria", 20))
        main_label.pack()

        left_container = Frame(self, highlightbackground=colors['gray'], highlightthickness=1)
        left_container.place(relx=0, rely=1, relwidth=0.35, relheight=0.92, anchor=SW)

        right_container = Frame(self)
        right_container.place(relx=1, rely=1, relwidth=0.65, relheight=0.92, anchor=SE)

        self.balance_container = Frame(left_container)
        self.balance_container.place(relx=0.5, rely=0.05, relheight=0.95, anchor=N)

        self.render_account_balance('0')

        balance_add_label = Label(self.balance_container, text='Doładuj konto kwotą: ')
        balance_add_label.config(font=("Aria", 14))
        balance_add_label.grid(row=1, column=0)

        self.balance_entry = Entry(self.balance_container)
        self.balance_entry.config(width=5)
        self.balance_entry.grid(row=1, column=1)

        balance_add_label2 = Label(self.balance_container, text='zł')
        balance_add_label2.config(font=("Aria", 14))
        balance_add_label2.grid(row=1, column=2, pady=10)

        balance_add_button = Button(self.balance_container, text='Doładuj', command=self.add_balance)
        balance_add_button.config(height=2, width=10)
        balance_add_button.grid(row=2, columnspan=3, pady=15)

        results_header_label = Label(right_container, text='Moje losy')
        results_header_label.config(font=("Aria", 17))
        results_header_label.pack()

        self.results_container = Frame(right_container)
        self.results_container.place(relx=0.5, rely=0.07, relheight=0.92, anchor=N)

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
            self.render_list_element(self.results_container, el['row'], el['column'], el['text'], 15, 10)

    def render_list_element(self, container, row, column, text, padx=0, pady=0):
        element = Label(container, text=text)
        element.config(font=("Aria", 12), padx=padx, pady=pady)
        element.grid(row=row, column=column)
        return element

    def get_user_coupons(self):
        self.controller.controller.send_request('MY_COUPONS')

    def get_account_balacne(self):
        self.controller.controller.send_request('GET_BALANCE')

    def render_account_balance(self, balance):
        self.balance_label.grid_forget()
        self.balance_label = Label(self.balance_container, text='Stan konta: ' + balance + 'zł')
        self.balance_label.config(font=("Aria", 14))
        self.balance_label.grid(row=0, columnspan=3)

    def add_balance(self):
        balance = self.balance_entry.get()
        check = balance.split('.')
        try:
            if len(balance) == 0 or len(check) >= 2 and len(check[1]) > 2 or float(balance) <= 0:
                messagebox.showinfo('Doładowywanie konta', 'Podaj dodatnią wartość z precyzją maksymalnie do dwóch miejsc po przecinku')
                return

            self.controller.controller.send_request('ADD_BALANCE ' + balance)
        except ValueError:
            messagebox.showinfo('Doładowywanie konta', 'Musisz podać wartość liczbową')

    def render_coupons(self, coupons):
        for el in self.list:
            el.grid_forget()
        self.list = []
        self.results_container.place_forget()
        self.results_container.place(relx=0.5, rely=0.07, relheight=0.92, anchor=N)
        row = 1
        for el in coupons:
            column = 0
            for el2 in el:
                element = self.render_list_element(self.results_container, row, column, el2, 6, 5)
                self.list.append(element)
                column += 1
            row += 1

    def reset(self):
        self.get_user_coupons()
        self.get_account_balacne()
