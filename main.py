from queue import Queue
from threading import Thread
import telebot
import time
from communicator import *
import datetime


with open('token.txt') as token_file:
    for token in token_file:
        break

    bot = telebot.TeleBot(token)


# A thread that communicates with chats
def communicator(queue):

    @bot.message_handler(commands=['greet'])
    def greet(message):
        c_greet(bot, message)

    @bot.message_handler(commands=['new_duty'])
    def new_duty(message):
        c_new_duty(bot, queue, message)

    bot.polling()
    print('communicator end')

# A thread that reminds chats about events
def reminder(queue):

    data_length = 3
    datas = [ {
        'chat_id': 1234,
        'type': 'new_duty',

        'name': 'test_duty',
        'frequency': datetime.timedelta(days=1),
        'start_time': datetime.datetime.utcnow()-datetime.timedelta(seconds=i*2),
        'flatmates': ['Ed', 'Clemens', 'Linda', 'Basti'],
        'message': 'Du bist dran '+str(i),
    }
    for i in range(data_length)]

    for data in datas: queue.put(data)

    dutys = []

    WAIT_TIME = 1 # seconds
    while True:

        # Check if there's anything in the queue
        queueWasNotEmpty = not queue.empty()
        while not queue.empty():
            print("We have new messages")

            #New messages!
            data = queue.get()

            if data['type']=='new_duty':
                dutys.append(chat_reminder_instance(data))

        if queueWasNotEmpty:
            dutys = sort_dutys(dutys)

        # Check if you have any dutys at all
        if len(dutys)==0:
            print("No dutys found. Waiting 1 second.")
            time.sleep(1)
            continue
        
        # Check if anything needs to run now
        dutysDone = []
        print("Looking through dutys")
        for duty in dutys:
            if duty.should_print_now():
                dutyToDo = dutys.pop(0)
                dutysDone.append(dutyToDo)
                message = duty.print_message_and_cycle()
                print(message)
            else:
                break
        # Add all the dutys that were printed to the end of the list
        for duty in dutysDone: dutys.append(duty)

        # Wait until it's time to check things again
        time.sleep(WAIT_TIME) 

def sort_dutys(dutys):
    datetimes = [duty.goal_datetime for duty in dutys]
    ref = datetime.datetime.utcnow()
    timedeltas = [(ref-dt).total_seconds() for dt in datetimes]
    dutys = [duty for _,duty in sorted(zip(timedeltas,dutys))]
    return dutys


class chat_reminder_instance():

    def __init__(self,item):
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


    




# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=communicator, args=(q,))
t2 = Thread(target=reminder, args=(q,))
t1.start()
t2.start()
