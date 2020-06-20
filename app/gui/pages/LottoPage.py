from tkinter import *
from app.gui.config import colors


class LottoPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.place(relwidth=1, relheight=1)
        self.controller = controller
        self.main_label = Label(self, text='Następne losowanie za')

        self.list = []

        # main_label = Label(self, text='Następne losowanie za ' + self.time_to_next_lottery)
        # main_label.config(font=("Aria", 20))
        # main_label.pack()

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

    def show_won_list(self, last_won):
        for el in self.list:
            el.grid_forget()
        self.list = []
        self.result_container.pack_forget()
        row = 1
        for el in last_won:
            column = 0
            for el2 in el:
                element = self.render_list_element(self.result_container, row, column, el2, 6, 5, colors['light_gray'])
                self.list.append(element)
                column += 1
            row += 1

    def get_last_won(self):
        self.controller.controller.send_request('WON_LIST')

    def get_time_to_next_lottery(self):
        self.controller.controller.send_request('GET_LOTTERY_DATE')

    def render_lottery_date(self, time):
        date = time.replace('&', ' ')
        self.main_label.pack_forget()
        self.main_label = Label(self, text='Następne losowanie: ' + date)
        self.main_label.config(font=("Aria", 18))
        self.main_label.pack()

    def render_list_element(self, container, row, column, text, padx=0, pady=0, bg=None):
        element = Label(container, text=text, bg=bg)
        element.config(font=("Aria", 11), padx=padx, pady=pady)
        element.grid(row=row, column=column)
        return element

    def reset(self):
        self.get_last_won()
        self.get_time_to_next_lottery()
