class Student:
    # def __init__(self, name):
    #     self.__name = name
    #
    # def get_name(self):
    #     return self.__name
    #
    # def set_name(self, new_name):
    #     self.__name = new_name
    #
    # def delete_name(self):                                              # описывает поведение del. можно запретить удалить, можно позволить удалить и не только
    #     raise Exception('Нельзя удалять name')
    #
    # name = property(get_name, set_name, delete_name)

    @property
    def __init__(self):
        return self.__name

    def get_name(self):
        return self.__name

    def set_name(self, new_name):
        self.__name = new_name

    def delete_name(self):
        raise Exception('Нельзя удалять name')

    name = property(get_name, set_name, delete_name)

s = Student('Asan')
# print(s.get_name())
# s.set_name('Hasan')
# print(s.get_name())
print(s.name)