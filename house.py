class House(object):
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.__roommates = []
        self.__duties = []

    def add_roommate(self, new_roommate):
        self.__roommates.append(new_roommate)

    def remove_roommate(self, old_roommate):
        self.__roommates.remove(old_roommate)

    def switch_roommates(self, old_roommate, new_roommate):
        self.add_roommate(new_roommate)
        self.remove_roommate(old_roommate)

    def get_dict_representation(self):
        return {
            self.chat_id: {
                'roommates': self.__roommates,
                'chat_id': self.chat_id,
            }
        }

    def add_duty(self, duty_name):
        self.__duties.append(Duty(duty_name))


class Duty(object):
    def __init__(self, name):
        self.name = name
        self.weekday = None
        self.list_names = None

    def set_weekday(self, weekday):
        if weekday not in range(7):
            return False
        self.weekday = weekday
        return True

    def config(self, house: House):
        pass


task = {
    'date': None,
    'person': None,
    'task_name': None
}
