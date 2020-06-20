from tkinter import *
from tkinter import messagebox
from app.gui.config import colors

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

        login_button = Button(register_container, text="Zaloguj się!", bg=colors['light_gray'], command=self.controller.navigation_to_login)
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

    def reset(self):
        pass
