from tkinter import *
from tkinter import messagebox
from app.gui.config import colors
from app.utils import Utils


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
        values_list = [self.entry_1.get(), self.entry_2.get(), self.entry_3.get(), self.entry_4.get(), self.entry_5.get(), self.entry_6.get()]
        values = list(set(values_list))
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
        else:
            self.controller.controller.send_request('COUPON_BUY ' + Utils.array_serializer(values_list))

    # def get_lotto_string(self, values_list):
    #     result = ''
    #     for el in values_list:
    #         result += el + ' '
    #     return result[:-1]

    def reset(self):
        pass
