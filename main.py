from queue import Queue
from threading import Thread
import telebot
import time

from communicator.general import c_greet, get_user_input
from communicator.new_duty import new_duty_input_infos
from communicator.handle_flatmates import swap_members_input_infos, exchange_members_input_infos

from reminder import DutyObject, sort_dutys, print_duty_list, save_dutys, load_dutys
from reminder_temp.general import find_duty, find_chat_dutys


with open('./token.txt') as token_file:
    for token in token_file:
        break
    token = token.rstrip()
    bot = telebot.TeleBot(token)

# A thread that communicates with chats
def communicator(queue):

    @bot.message_handler(commands=['test'])
    def greet(message):
        c_greet(bot, message)
        print(message)

    @bot.message_handler(commands=['new_duty'])
    def new_duty(message):
        get_user_input(bot, queue, message, new_duty_input_infos, data_type='new_duty')

    @bot.message_handler(commands=['exchange_flatmates'])
    def change_flatmates(message):
        get_user_input(bot, queue, message, exchange_members_input_infos, data_type='exchange_members')

    @bot.message_handler(commands=['swap_flatmates'])
    def swap_flatmates(message):
        get_user_input(bot, queue, message, swap_members_input_infos, data_type='swap_members')

    bot.polling()
    print('communicator end')


# A thread that reminds chats about events
def reminder(queue):

    dutys = load_dutys()

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
            elif data['type'] == 'new_duty':
                dutys.append(DutyObject(bot, data))

            # exchange members for all duties
            elif data['type'] == 'exchange_members':
                chat_dutys = find_chat_dutys(data['chat_id'], dutys)
                for duty in chat_dutys:
                    duty.exchange_member(data['new_member'], data['old_member'])

            # swap members for one duty
            elif data['type'] == 'swap_members':
                chat_dutys = find_chat_dutys(data['chat_id'], dutys)
                duty = find_duty(data['duty_name'], chat_dutys)
                duty.swap_members(data['member1'], data['member2'])

            elif data['type'] == 'print_duty_list':
                print_duty_list(dutys)

        if queueWasNotEmpty:
            dutys = sort_dutys(dutys)
            save_dutys(dutys)

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
