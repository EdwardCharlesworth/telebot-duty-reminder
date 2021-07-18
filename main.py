from queue import Queue
from threading import Thread
import telebot
import time
from communicator import *


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
    while True:
        time.sleep(60*10)
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