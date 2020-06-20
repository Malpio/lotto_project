from tkinter import *
from app.gui.config import colors
from app.gui.pages.LottoBuyPage import LottoBuyPage
from app.gui.pages.LoginPage import LoginPage
from app.gui.pages.MyAccountPage import MyAccountPage
from app.gui.pages.LottoPage import LottoPage



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

        self.set_first_page(LottoPage)

    def logout(self):
        self.controller.reset_stack_then_navigate(LoginPage)

    def navigation(self, context):
        if len(self.navigation_stack) >= 1:
            prev = self.navigation_stack[-1]
            prev.pack_forget()
        frame = self.frames[context]
        context.reset(frame)
        self.navigation_stack.append(frame)
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()

    def set_first_page(self, context):
        frame = self.frames[context]
        self.navigation_stack.append(frame)
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()

    def reset(self):
        pass
