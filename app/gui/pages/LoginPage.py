from tkinter import *
from tkinter import messagebox
from app.gui.config import colors


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

        register_button = Button(register_container, text="Zarejestruj się!", bg=colors['light_gray'], command=self.controller.navigation_to_register)
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

    def reset(self):
        pass
