from queue import Queue
from threading import Thread
import telebot
import time
from communicator import communicate


with open('token.txt') as token_file:
    for token in token_file:
        break

    bot = telebot.TeleBot(token)


# A thread that consumes data
def communicator(queue,):
    while True:
        queue.put(data)


# A thread that produces data
def reminder(queue):
    date_list = []
    while True:
        time.sleep(60)
        # Produce some data
        data = queue.get()
        date_list = sort_function(date_list, data)
        if is_today(date_list[0]):
            data = date_list.pop()
            bot.send





# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=communicator, args=(q,))
t2 = Thread(target=reminder, args=(q,))
t1.start()
t2.start()