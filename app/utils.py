class Utils:
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
