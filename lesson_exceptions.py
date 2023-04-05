# num = input('Введите число от 1 до 7: ')
#
# if int(num) > 7 or int(num) < 1:
#     raise Exception('Введите дни недели от 1 до 7')
#
# weekdays = {
#     '1': 'Monday',
#     '2': 'Tuesday',
#     '3': 'Wednesday',
#     '4': 'Thursday',
#     '5': 'Friday',
#     '6': 'Saturday',
#     '7': 'Sunday'
# }
#
# print(weekdays[num])


import datetime


class PersonAgeException(Exception):
    def __init__(self, age, message=None):
        self.age = age
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return f'введенный вами возраст {self.age} не соответствует реальному возрасту. {self.age} не должно быть ' \
               f'меньше нуля'


def get_birth_year(age):
    age = int(age)
    if age < 0:
        raise PersonAgeException(age)
    this_year = datetime.date.today()
    birth_year = this_year.year - age
    return birth_year

if __name__ == '__main__':
    errors = dict()
    while True:
        age = input('ваш возраст?')
        try:
            birth_year = get_birth_year(age)
        except PersonAgeException as e:
            errors['error'] = e
        except ValueError:
            print('вводите числовые значения')
        else:
            print(birth_year)
            break
        finally:
            print(errors)