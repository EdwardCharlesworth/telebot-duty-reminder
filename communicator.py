import requests
import json
import telebot
import datetime
import re


max_tries = 5


class AbortInput(Exception):
    pass


def c_greet(bot, message):
    bot.send_message(message.chat.id, 'Hello there!')


def c_new_duty(bot, queue, message):
    chat_id = message.chat.id

    data = {
        'chat_id': chat_id,
        'type': 'new_duty',

        'temp_input': None,

        'name': 'defaultname',
        'start_time': datetime.datetime.utcnow(),
        'frequency': datetime.timedelta(days=1),
        'message': 'Du bist dran',
        'flatmates': ['Ed', 'Clemens', 'Linda', 'Basti'],
    }

    infos = [{
        'key': 'name',
        'message': "What's your duty's name?",
        'pre_func': [str],
    }, {
        'key': 'start_time',
        'message': f"When should the duty start (HH:MM dd.mm.yyyy)?",
        'pre_func': [pre_start_time],
    }, {
        'key': 'frequency',
        'message': f"In which frequency do you want to be reminded (in days)?",
        'pre_func': [int, datetime.timedelta],
    }, {
#        'key': 'message',
#        'message': f"Please enter a message to ?",
#        'pre_func': [str],
#    }, {
        'key': 'flatmates',
        'message': f"What are your flatmates (order matters)?",
        #'message': f"Add a name of a flatmate (... or exit with 'exit').",
        'pre_func': [find_flatmates],
        #'iterations': 50,
    }]

    def key_handler(message, current_info, data, infos):
        """

        :param message:
        :param current_info:    dict with infos how the next answer should be processed
        :param data:            dict that should be filled for reminder
        :param infos:           list(dicts) that will be used to get user input (for data)
        :return:
        """
        value = message.text[1:]
        if value == 'exit':
            return

        # apply individual functions to input value
        for pre_func in current_info['pre_func']:
            value = pre_func(value)
        data[current_info['key']] = value

        try:
            # get next info
            current_info = infos.pop(0)
        except IndexError:
            # end with sending data to reminder
            queue.put(data)
            return

        sent_msg = bot.reply_to(message, current_info['message'])
        bot.register_next_step_handler(sent_msg, key_handler, current_info, data, infos)

    current_info = infos.pop(0)
    sent_msg = bot.reply_to(message, current_info['message'])
    bot.register_next_step_handler(sent_msg, key_handler, current_info, data, infos)




# ### helpers

def pre_start_time(start_time):
    start_time = datetime.datetime.strptime(start_time, '%H:%M %d.%m.%Y')
    if datetime.datetime.utcnow().date() > start_time.date():
        raise NotImplementedError
    return start_time


def find_flatmates(flatmates_string):
    flatmates_list = re.split(',| |/', flatmates_string)
    return flatmates_list


### for later use
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#def gen_markup():
#    markup = InlineKeyboardMarkup()
#    markup.row_width = 2
#    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                               InlineKeyboardButton("No", callback_data="cb_no"))
#    return markup
