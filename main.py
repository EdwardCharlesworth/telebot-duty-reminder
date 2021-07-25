from queue import Queue
from threading import Thread
import time

from custom_telebot import CustomTeleBot
from dump_and_load_json import load_dutys, save_dutys
from prod_help import endless_try

from communicator.helper import load_dutys_of_chat
from communicator.general import c_greet, get_user_input
from communicator.handle_duties import new_duty_input_infos, delete_duty_input_infos, \
    list_duty_input_infos, additional_message_input_text
from communicator.handle_flatmates import swap_members_input_infos, exchange_member_input_infos, \
    add_member_input_infos, add_duty_member_input_infos, remove_member_input_infos

from reminder.duty_class import DutyObject
from reminder.helper import find_duty, find_chat_dutys


with open('./token.txt') as token_file:
    for token in token_file:
        break
    token = token.rstrip()
    bot = CustomTeleBot(token, num_threads=4)


# A thread that communicates with chats
@endless_try
def communicator(queue):

    # handle duties

    @bot.message_handler(commands=['new_duty'])
    def new_duty(message):
        get_user_input(bot, queue, message, new_duty_input_infos.copy(), data_type='new_duty')

    @bot.message_handler(commands=['delete_duty'])
    def delete_duty(message):
        get_user_input(bot, queue, message, delete_duty_input_infos.copy(), data_type='delete_duty')

    @bot.message_handler(commands=['additional_message'])
    def additional_message(message):
        get_user_input(bot, queue, message, additional_message_input_text.copy(), data_type='additional_message')

    @bot.message_handler(commands=['list_duties'])
    def list_duties(message):
        help_message = """There are no duties active"""
        duty_dicts = load_dutys_of_chat(chat_id=message.chat.id)
        if duty_dicts:
            help_message = f"""Following duties are active:\n"""
            help_message += '\n'.join([duty_dict['name']+': Next up '+duty_dict['flatmates'][0]
                                       for duty_dict in duty_dicts])
        bot.send_message(message.chat.id, help_message)

    @bot.message_handler(commands=['get_duty_info'])
    def get_duty_info(message):
        get_user_input(bot, queue, message, list_duty_input_infos.copy(), data_type='NOTHING')

    # multi member operators

    @bot.message_handler(commands=['exchange_member'])
    def exchange_member(message):
        get_user_input(bot, queue, message, exchange_member_input_infos.copy(), data_type='exchange_member')

    @bot.message_handler(commands=['swap_members'])
    def swap_members(message):
        get_user_input(bot, queue, message, swap_members_input_infos.copy(), data_type='swap_members')

    # single member operators

    @bot.message_handler(commands=['add_member'])
    def add_member(message):
        get_user_input(bot, queue, message, add_member_input_infos.copy(), data_type='add_member')

    @bot.message_handler(commands=['add_duty_member'])
    def add_member(message):
        get_user_input(bot, queue, message, add_duty_member_input_infos.copy(), data_type='add_member')

    @bot.message_handler(commands=['remove_member'])
    def remove_member(message):
        get_user_input(bot, queue, message, remove_member_input_infos.copy(), data_type='remove_member')

    # general

    @bot.message_handler(commands=['start', 'greet'])
    def greet(message):
        c_greet(bot, message)
        print(message)

    @bot.message_handler(func=lambda m: True)
    def help(message):
        help_message = f"""
/new_duty - will add a new duty
/delete_duty - will delete one or all duties
/additional_message - will add an additional message to the standard reminder message
/list_duties - will return a list of all duties
/get_duty_info - will return detailed info regarding one duty

/exchange_member - will exchange an old member with a new one for all duties
/swap_members - will swap two members in the order of one duty

/add_member - will add a new member to one or all duties
/add_duty_member - will add a member to one duty
/remove_member - will remove a member from one or all duties
"""
        bot.send_message(message.chat.id, help_message)

    bot.polling()
    print('communicator end')


# A thread that reminds chats about events
@endless_try
def reminder(queue):

    dutys = load_dutys(bot)

    WAIT_TIME = 1  # seconds
    while True:

        # Check if there's anything in the queue
        queueWasEmpty = True
        while not queue.empty():
            #New messages!
            data = queue.get()
            queueWasEmpty = False
            print("New messages of type: "+data['type'])

            if any( [data[key] == None for key in data.keys()] ):
                print("FOUND AN INCOMPLETE ENTRY")
                continue

            elif data['type'] == 'new_duty':
                dutys.append(DutyObject(bot, data))

            elif data['type'] == 'delete_duty':
                for duty in find_chat_dutys(data['chat_id'], dutys):
                    if data['name'] == 'ALL' or data['name'] == duty.name:
                        dutys.remove(duty)
                save_dutys(dutys)

            # add member
            elif data['type'] == 'add_member':
                for duty in find_chat_dutys(data['chat_id'], dutys):
                    if data['name'] == 'ALL' or data['name'] == duty['name']:
                        duty.add_member(data['new_member'])

            # delete member
            elif data['type'] == 'remove_member':
                for duty in find_chat_dutys(data['chat_id'], dutys):
                    if data['name'] == 'ALL' or data['name'] == duty['name']:
                        duty.delete_member(data['old_member'])

            # exchange member for all duties
            elif data['type'] == 'exchange_member':
                chat_dutys = find_chat_dutys(data['chat_id'], dutys)
                for duty in chat_dutys:
                    duty.exchange_member(data['old_member'], data['new_member'])

            # swap members for one duty
            elif data['type'] == 'swap_members':
                chat_dutys = find_chat_dutys(data['chat_id'], dutys)
                duty = find_duty(data['name'], chat_dutys)
                duty.swap_members(data['member1'], data['member2'])

            elif data['type'] == 'additional_message':
                chat_dutys = find_chat_dutys(data['chat_id'], dutys)
                duty = find_duty(data['name'], chat_dutys)
                duty.additional_message = data['message']

        if not queueWasEmpty:
            dutys = sorted(dutys)

        # Check if you have any dutys at all
        if len(dutys)==0:
            # print("No dutys found. Waiting 1 second.")
            time.sleep(1)  # TODO finalize
            continue
        
        # Check if anything needs to run now
        dutysDone = []
        something_was_updated = False
        # print("Looking through dutys")
        for duty in dutys:
            if duty.should_print_now():
                message = duty.print_message_and_cycle()
                something_was_updated = True
            else:
                break
        # Add all the dutys that were printed to the end of the list
        # for duty in dutysDone: dutys.append(duty)
        dutys = sorted(dutys)
        if not queueWasEmpty or something_was_updated:
            save_dutys(dutys)

        # Wait until it's time to check things again
        time.sleep(WAIT_TIME) 

    print('reminder end')


# Create the shared queue and launch both threads


q = Queue()
t1 = Thread(target=communicator, args=(q,))
t2 = Thread(target=reminder, args=(q,))
t1.start()
t2.start()
