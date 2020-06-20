import time
from app.config import lottery_time


class Utils:
    @staticmethod
    def get_lottery_date():
        days = time.localtime().tm_mday
        months = time.localtime().tm_mon
        years = time.localtime().tm_year
        hours = time.localtime().tm_hour
        mins = time.localtime().tm_min + lottery_time
        secs = time.localtime().tm_sec
        if days < 10:
            days = "0" + str(days)
        if months < 10:
            months = "0" + str(months)
        if hours < 10:
            hours = "0" + str(hours)
        if mins < 10:
            mins = "0" + str(mins)
        if secs < 10:
            secs = "0" + str(secs)
        return str(days) + "/" + str(months) + "/" + str(years) + " " + str(hours) + ":" + str(mins) + ":" + str(secs)

    @staticmethod
    def to_array(string):
        return string.split(' ')

    @staticmethod
    def to_string(array):
        result = ''
        for el in array:
            result += el + ' '
        return result[:-1]

    @staticmethod
    def numbers_in_range(array):
        try:
            for el in array:
                if int(el) < 1 or int(el) > 49:
                    return False
            return True
        except:
            return False

    @staticmethod
    def number_unique(array):
        unique_array = list(dict.fromkeys(array))
        return len(unique_array) == len(array)

    @staticmethod
    def get_count_of_same_numbers(won_numbers, coupon_numbers):
        count = 0
        for won_number in won_numbers:
            for coupon_number in coupon_numbers:
                if won_number == coupon_number:
                    count += 1
                    break
        return count

    @staticmethod
    def serializer(to_serialize):
        result = ''
        for l in to_serialize:
            res_el = ''
            for el in l:
                res_el += str(el) + ','
            result += res_el[:-1] + '&'
        result = result.replace(' ', '<!>')
        return result[:-1]

    @staticmethod
    def deserializer(to_deserialize):
        to_deserialize = to_deserialize.replace('<!>', ' ')
        array = to_deserialize.split('&')
        result = []
        for el in array:
            insite_list = el.split(',')
            result.append(insite_list)
        return result

    @staticmethod
    def array_serializer(to_serialize):
        result = ''
        for el in to_serialize:
            result += el + '&'
        return result[:-1]

    @staticmethod
    def array_deserializer(to_deserialize):
        result = to_deserialize.split('&')
        return result
