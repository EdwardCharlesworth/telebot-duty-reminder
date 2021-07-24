import datetime


def sort_dutys(dutys):
    datetimes = [duty.goal_datetime for duty in dutys]
    ref = datetime.datetime.utcnow()
    timedeltas = [(ref-dt).total_seconds() for dt in datetimes]
    dutys = [duty for _,duty in sorted(zip(timedeltas,dutys))]
    return dutys


class Duty():

    def __init__(self, item):
        self.chat_id = item['chat_id']
        self.duty_name = item['name']
        self.frequency = item['frequency'].days/(24*60*4)
        self.goal_datetime = item['start_time']
        self.roster = item['flatmates']
        self.message = item['message']

    def should_print_now(self):
        goal = self.goal_datetime
        now = datetime.datetime.utcnow()
        if (now-goal).total_seconds() > 0:
            return True
        else:
            return False

    def print_message_and_cycle(self):
        member = self.roster.pop(0) #Pull the member whose turn it is
        message = member+": "+self.message#Write the message
        self.roster.append(member) #Add member whose turn it is to the roster
        # Calculate the next time you need to write
        next_datetime = self.goal_datetime + datetime.timedelta(days=self.frequency)
        self.goal_datetime = next_datetime # Set that time
        return message
