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

    data = {
        'chat_id': 1234,
        'type': 'new_duty',

        'name': 'test_duty',
        'frequency': datetime.timedelta(days=1),
        'start_time': datetime.datetime.utcnow(),
        'flatmates': ['Ed', 'Clemens', 'Linda', 'Basti'],
        'message': 'Du bist dran',
    }
    queue.put(data)

    items = []

    WAIT_TIME = 5 # seconds
    while True:

        # Check if there's anything in the queue
        if not queue.empty():
            print("Got new messages")

            #New messages!
            data = queue.get()

            if data['type']=='new_duty':
                items.append(chat_reminder_instance(data))

            #date_list = sort_function(date_list, data)

        # Check if you have any items at all
        if len(items)==0:
            print("No items found. Waiting 1 second.")
            time.sleep(1)
            continue
        
        # Check if anything needs to run now
        for item in items:
            print("Looking through items")
            if item.should_print_now():
                print("Time to print")
                message = item.print_message_and_cycle()
                print(message)
            #else:
            #    break
            # This is where you should set something up so
            # that you don't run through the list constantly.
            # Sort the list items by when they need to happen.
            # Then, when they happen, move them to the end of
            # the item list. So then you only need to check
            # items until you find one where you don't need to
            # do anything. Then all the following items don't
            # need anything either.

        # Wait until it's time to check things again
        time.sleep(WAIT_TIME) 

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
        next_datetime = self.goal_datetime + datetime.timedelta(days=self.frequency)
        self.goal_datetime = next_datetime
        return message


    




# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=communicator, args=(q,))
t2 = Thread(target=reminder, args=(q,))
t1.start()
t2.start()
