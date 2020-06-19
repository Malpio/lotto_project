import sqlite3
from datetime import datetime
from app.config import date_format, lotto_price
from app.utils import Utils


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('lotto.db')
        self.cursor = self.connection.cursor()

    def register(self, first_name, last_name, login, password):
        print('passw', password)
        try:

            self.cursor.execute('insert into users (first_name, last_name, login, password) values (?,?,?,?)',
                                (first_name, last_name, login, password))

            self.connection.commit()
            return {'response': 'REGISTER REGISTER_OK'}
        except sqlite3.Error as e:
            print('error ', e)
            return {'response': 'REGISTER USERNAME_ALREADY_EXIST'}

    def login(self, login, password):
        self.cursor.execute('select * from users where login = ? and password = ?', (login, password))
        user = self.cursor.fetchone()
        if user:
            return {'response': 'LOGIN LOGIN_OK', 'user_id': user[0]}
        else:
            return {'response': 'LOGIN LOGIN_FAIL'}

    def get_user(self, user_id):
        try:
            self.cursor.execute('select * from users where user_id = ?', (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error:
            return None

    def get_balance(self, user_id):
        user = self.get_user(user_id)
        if user:
            balance = str(user[3])
            return {'response': 'GET_BALANCE ' + balance}
        else:
            return {'response': 'UNEXPECTED_ERROR'}

    def add_balance(self, user_id, amount):
        update_balance_status = self.update_balance(user_id, amount)
        if update_balance_status:
            return {'response': 'BALANCE BALANCE_ADDED'}
        else:
            return {'response': 'UNEXPECTED_ERROR'}

    def check_balance_enough(self, user_id):
        user = self.get_user(user_id)
        if user and user[3] >= lotto_price:
            return True
        return False

    def update_balance(self, user_id, amount):
        user = self.get_user(user_id)
        if user:
            try:
                new_balance = user[3] + amount
                self.cursor.execute('update users set balance = ? where user_id = ?', (new_balance, user_id))
                self.connection.commit()
                return True
            except sqlite3.Error:
                return False
        else:
            return False

    def create_lotto(self):
        try:
            self.cursor.execute(
                'insert into lotto (count_of_three, count_of_four, count_of_five, count_of_six) values (?,?,?,?)',
                (0, 0, 0, 0))
            self.connection.commit()
            return True
        except sqlite3.Error:
            return False

    def update_lotto_after_lottery(self, lotto_id, won_numbers):
        try:
            now = datetime.now()
            lottery_date = now.strftime(date_format)
            serialize_numbers = Utils.to_string(won_numbers)
            counts_of_winners = self.get_count_of_winners(lotto_id, won_numbers)
            self.cursor.execute('update lotto set won_numbers = ?, ' +
                                'lottery_date = ?, count_of_three = ?, ' +
                                'count_of_four = ?, count_of_five = ?, ' +
                                'count_of_six = ? where lotto_id = ?',
                                (serialize_numbers, lottery_date,
                                 counts_of_winners['count_of_three'], counts_of_winners['count_of_four'],
                                 counts_of_winners['count_of_five'], counts_of_winners['count_of_six'], lotto_id))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            return e

    def buy_coupon(self, lotto_id, user_id, numbers):
        if len(numbers) != 6 or not Utils.numbers_in_range(numbers) or not Utils.number_unique(numbers):
            return {'response': 'COUPON_BUY COUPON_INVALID_NUMBERS'}

        try:
            if self.check_balance_enough(user_id):
                if self.update_balance(user_id, lotto_price * (-1)):
                    now = datetime.now()
                    bought_date = now.strftime(date_format)
                    serialize_numbers = Utils.to_string(numbers)
                    self.cursor.execute(
                        'insert into coupons (bought_date, lotto_id, user_id, numbers) values (?,?,?,?)',
                        (bought_date, lotto_id, user_id, serialize_numbers))
                    self.connection.commit()
                    return {'response': 'COUPON_BUY COUPON_BUY_OK'}
                else:
                    return {'response': 'UNEXPECTED_ERROR'}
            else:
                return {'response': 'COUPON_BUY NO_ENOUGH_BALANCE'}
        except sqlite3.Error:
            return {'response': 'UNEXPECTED_ERROR'}

    def get_coupons(self, lotto_id):
        try:
            self.cursor.execute('select * from coupons where lotto_id = ?', (lotto_id,))
            return self.cursor.fetchall()
        except:
            return []

    def get_count_of_winners(self, lotto_id, won_numbers):
        count_of_three = 0
        count_of_four = 0
        count_of_five = 0
        count_of_six = 0
        try:
            coupons_list = self.get_coupons(lotto_id)
            for coupon in coupons_list:
                numbers = Utils.to_array(coupon[4])
                count_of_same_number = Utils.get_count_of_same_numbers(won_numbers, numbers)
                if count_of_same_number == 3:
                    count_of_three += 1
                elif count_of_same_number == 4:
                    count_of_four += 1
                elif count_of_same_number == 5:
                    count_of_five += 1
                elif count_of_same_number == 6:
                    count_of_six += 1

            return {'count_of_three': count_of_three, 'count_of_four': count_of_four, 'count_of_five': count_of_five,
                    'count_of_six': count_of_six}
        except:
            return {'count_of_three': count_of_three, 'count_of_four': count_of_four, 'count_of_five': count_of_five,
                    'count_of_six': count_of_six}

    def get_user_coupons(self, user_id):
        try:
            self.cursor.execute('select * from coupons where user_id = ? order by coupon_id desc', (user_id,))
            return self.cursor.fetchall()
        except sqlite3.Error:
            return None

    def get_user_coupons_list_with_lottery(self, user_id):
        result = []
        coupons_list = self.get_user_coupons(user_id)
        if not list:
            return {'response': 'UNEXPECTED_ERROR'}
        for el in coupons_list:
            one_element = []
            one_element.append(el[1])
            one_element.append(el[4])
            lotto = self.get_lotto_by_id(el[2])
            if not lotto:
                print('qwe')
                return {'response': 'UNEXPECTED_ERROR'}
            one_element.append(lotto[0])
            one_element.append(lotto[1])
            result.append(one_element)
        result = Utils.serializer(result)
        return {'response': 'MY_COUPONS ' + result}

    def get_lotto_by_id(self, lotto_id):
        try:
            self.cursor.execute(
                'select IFNULL(won_numbers, "brak"), IFNULL(lottery_date, "brak") from lotto where lotto_id = ?',
                (lotto_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
            return None

    def get_last_lotto(self, count):
        try:
            self.cursor.execute('select * from lotto where won_numbers is not null order by lotto_id desc')
            last_won = Utils.serializer(self.cursor.fetchmany(count))
            return {'response': 'LAST_WON ' + last_won}
        except sqlite3.Error as e:
            return {'response': 'UNEXPECTED_ERROR'}

    def get_won_list(self):
        try:
            self.cursor.execute(
                'select lottery_date , main_prize, won_numbers, count_of_three, count_of_four, count_of_five, count_of_six from lotto where won_numbers is not null order by lotto_id desc')
            won_list = Utils.serializer(self.cursor.fetchall())
            return {'response': 'WON_LIST ' + won_list}
        except sqlite3.Error as e:
            print(e)
            return {'response': 'UNEXPECTED_ERROR'}

    def get_last_lottery_id(self):
        try:
            self.cursor.execute(
                'select lotto_id from lotto order by lotto_id desc limit 1')
            won_list = Utils.serializer(self.cursor.fetchall())
            return {'response': 'WON_LIST ' + won_list}
        except sqlite3.Error as e:
            print(e)
            return {'response': 'UNEXPECTED_ERROR'}