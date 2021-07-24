import datetime


def sort_dutys(dutys):
    datetimes = [duty.goal_datetime for duty in dutys]
    ref = datetime.datetime.utcnow()
    timedeltas = [(ref-dt).total_seconds() for dt in datetimes]
    dutys = [duty for _,duty in sorted(zip(timedeltas,dutys))]
    return dutys

def print_duty_list(dutys):
    for duty in dutys:
        print(duty.dump_information())

class DutyObject():

    def __init__(self, item):
        self.chat_id = item['chat_id']
        self.duty_name = item['name']
        self.frequency = item['frequency'].days/(24*60*4)
        self.goal_datetime = item['start_time']
        self.roster = item['flatmates']
        self.message = item['message']

    def dump_information(self):
        message  = 'Chat ID: '+self.chat_id+';'
        message += 'Duty Name: '+self.duty_name+';'
        message += 'Frequency: '+self.frequency+';'
        message += 'Next Reminder Date: '+self.goal_datetime.strftime("%m/%d/%Y, %H:%M:%S")+';'
        message += 'Roster: '+self.make_roster_string()+';'
        message += 'Reminder message: ('+self.message+').'
        return message

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

    def make_roster_message(self):
        message = ""
        for member in self.roster: message += member + ' '
        return message

    def change_roster(self):
        # self.roster = whatever function basti has
        return "Can't do this yet. Use whatever function Basti wrote to read in the flatmates."

    def change_message(self,message):
        self.message = message
        message = "Message is now: "+message
        return message

    def mitglied_tauschen(self,member1,member2):
        #Switching order of existing members
        #One problem here is that you really should afterwards go back to the original order
        #if two people do a one-time switch.
        message = ''
        ERROR = False
        if member1 not in self.roster: 
            message += " Could not find "+member1+"."
            ERROR = True
        if member2 not in self.roster: 
            message += " Could not find "+member2+"."
            ERROR = True
        if ERROR:
            return message
        else:
            index1=self.roster.index(member1)
            index2=self.roster.index(member2)
            message = "Mitglieder "+membe1+" und "+member2+" sind getauscht. Reinfolge ist jetzt: "
            message += self.make_roster_message()
            return message

    def mitglied_austauschen(self,memberOld,memberNew):
        # If somebody moves out, for example
        if member not in self.roster: 
            message += "Could not find "+memberOld+"."
            return message
        else:
            index = self.roster.index(memberOld)
            self.roster[index] = memberNew
            message += "Mitglied "+memberNew+" hat die Platz für "+memberOld+" genommen. Tschüss "+memberOld+"! Hat viel Spaß gemacht mit dir! Reinfolge ist jetzt: "
            message += self.make_roster_message()
            return message

    def mitglied_entfernen(self,member):
        # If somebody moves out, for example
        if member not in self.roster: 
            message += "Could not find "+member+"."
            return message
        else:
            self.roster.pop(member)
            message += "Mitglied "+member+" war von Listen entfernt. Tschüss "+member+"! Hat viel Spaß gemacht mit dir! Reinfolge ist jetzt: "
            message += self.make_roster_message()
            return message

    def mitglied_hinzufuegen(self,member):
        # If somebody moves in, for example
        self.roster.append(member)
        message += "Mitglied "+member+" war hinzugefügt. Hallo "+member+"! Reinfolge ist jetzt: "
        message += self.make_roster_message()
        return message

 
