import datetime
import json

def sort_dutys(dutys):
    datetimes = [duty.start_time for duty in dutys]
    ref = datetime.datetime.utcnow()
    timedeltas = [(ref-dt).total_seconds() for dt in datetimes]
    dutys = [duty for _,duty in sorted(zip(timedeltas,dutys))]
    return dutys


def print_duty_list(dutys):
    for duty in dutys:
        print(duty.dump_information())

def save_dutys(dutys):
    with open("dutybot_database.json","w") as file:
        # ensure that bot is not dumped (not possible)
        file.write(json.dumps([
            {key: value
             for key, value in duty.__dict__.items() if key != 'bot'}
            for duty in dutys
        ]))

def load_dutys(bot):
    databaseName = "dutybot_database.json"
    try:
        with open(databaseName,"r") as file:
            duty_dicts = json.load(file)
    except:
        print("Could not find database ("+databaseName+"). Duty list is empty.")
        duty_dicts = []

    dutys = []
    for duty_dict in duty_dicts:
        dutys.append(DutyObject(bot, item=duty_dict))

    return dutys

class DutyObject:

    def __init__(self, bot, item):
        self.bot = bot
        self.chat_id = item['chat_id']  # @Ed: don't change 'chat_id' to a different name!!!
        self.name = item['name']  # @Ed: don't change 'name' to a different name!!!
        if isinstance(item['frequency'], datetime.timedelta):
            self.frequency = item['frequency'].days/(24*60*4)
        else:
            self.frequency = item['frequency']
        self.start_time = item['start_time']
        self.flatmates = item['flatmates']  # @Ed: don't change 'flatmates' to a different name!!!
        self.message = item['message']

    def dump_information(self):
        message  = 'Chat ID: '+self.chat_id+';'
        message += 'Duty Name: '+self.name+';'
        message += 'Frequency: '+self.frequency+';'
        message += 'Next Reminder Date: ' + self.start_time.strftime("%m/%d/%Y, %H:%M:%S") + ';'
        message += 'Flatmates: '+self.make_roster_string()+';'
        message += 'Reminder message: ('+self.message+').'
        return self.send_message(message)

    def should_print_now(self):
        goal = self.start_time
        now = datetime.datetime.utcnow()
        if (now-goal).total_seconds() > 0:
            return True
        else:
            return False

    def print_message_and_cycle(self):
        member = self.flatmates.pop(0) #Pull the member whose turn it is
        message = member+": "+self.message#Write the message
        self.flatmates.append(member) #Add member whose turn it is to the roster
        # Calculate the next time you need to write
        next_datetime = self.start_time + datetime.timedelta(days=self.frequency)
        self.start_time = next_datetime # Set that time
        return self.send_message(message)

    def make_roster_message(self):
        message = ""
        for member in self.flatmates: message += member + ' '
        return self.send_message(message)

    def change_roster(self):
        # self.roster = whatever function basti has
        return "Can't do this yet. Use whatever function Basti wrote to read in the flatmates."

    def change_message(self,message):
        self.message = message
        message = "Message is now: "+message
        return self.send_message(message)

    def swap_members(self,member1,member2):
        #Switching order of existing members
        #One problem here is that you really should afterwards go back to the original order
        #if two people do a one-time switch.
        message = ''
        ERROR = False
        if member1 not in self.flatmates:
            message += " Could not find "+member1+"."
            ERROR = True
        if member2 not in self.flatmates:
            message += " Could not find "+member2+"."
            ERROR = True
        if ERROR:
            return self.send_message(message)
        else:
            index1=self.flatmates.index(member1)
            index2=self.flatmates.index(member2)
            message = "Mitglieder "+member1+" und "+member2+" sind getauscht. Reinfolge ist jetzt: "
            message += self.make_roster_message()
            return self.send_message(message)

    def exchange_member(self,memberOld,memberNew):
        # If somebody moves out, for example
        if memberOld not in self.flatmates:
            message = "Could not find "+memberOld+"."
            return self.send_message(message)
        else:
            index = self.flatmates.index(memberOld)
            self.flatmates[index] = memberNew
            message = "Mitglied "+memberNew+" hat die Platz für "+memberOld+" genommen. Tschüss "+memberOld+"! Hat viel Spaß gemacht mit dir! Reinfolge ist jetzt: "
            message += self.make_roster_message()
            return self.send_message(message)

    def delete_member(self,member):
        # If somebody moves out, for example
        if member not in self.flatmates:
            message = "Could not find "+member+"."
            return self.send_message(message)
        else:
            self.flatmates.pop(member)
            message = "Mitglied "+member+" war von Listen entfernt. Tschüss "+member+"! Hat viel Spaß gemacht mit dir! Reinfolge ist jetzt: "
            message += self.make_roster_message()
            return self.send_message(message)

    def add_member(self,member):
        # If somebody moves in, for example
        self.flatmates.append(member)
        message = "Mitglied "+member+" war hinzugefügt. Hallo "+member+"! Reinfolge ist jetzt: "
        message += self.make_roster_message()
        return self.send_message(message)

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)


pass