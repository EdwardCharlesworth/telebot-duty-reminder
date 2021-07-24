from queue import Queue
from threading import Thread
import telebot
import time

from communicator import AbortInput, c_new_duty, c_greet
from reminder import DutyObject, sort_dutys, print_duty_list


with open('token.txt') as token_file:
    for token in token_file:
        break

    bot = telebot.TeleBot(token)


# A thread that communicates with chats
def communicator(queue):

    @bot.message_handler(commands=['greet'])
    def greet(message):
        c_greet(bot, message)
        print(message)

    @bot.message_handler(commands=['new_duty'])
    def new_duty(message):
        try:
            c_new_duty(bot, queue, message)
        except AbortInput:
            bot.send_message(message.chat.id, f"Command was aborted.")

    bot.polling()
    print('communicator end')


# A thread that reminds chats about events
def reminder(queue):

    dutys = []

    WAIT_TIME = 1  # seconds
    while True:

        # Check if there's anything in the queue
        queueWasNotEmpty = not queue.empty()
        while not queue.empty():
            print("We have new messages")

            #New messages!
            data = queue.get()

            if any( [data[key] == None for key in data.keys()] ):
                print("FOUND AN INCOMPLETE ENTRY")
                continue
            elif data['type']=='new_duty':
                dutys.append(DutyObject(bot, data))
            elif data['type']=='print_duty_list':
                print_duty_list(dutys)

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
                message = duty.print_message_and_cycle()
                print(message)
            else:
                break
        # Add all the dutys that were printed to the end of the list
        # for duty in dutysDone: dutys.append(duty)
        dutys = sort_dutys(dutys)

        # Wait until it's time to check things again
        time.sleep(WAIT_TIME) 


    




# Create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=communicator, args=(q,))
t2 = Thread(target=reminder, args=(q,))
t1.start()
t2.start()
