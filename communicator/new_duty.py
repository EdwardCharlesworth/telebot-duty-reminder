import requests
import json
import telebot
import datetime
import re

from communicator.general import AbortInput, add_abort_message


def c_new_duty(bot, queue, message):
    chat_id = message.chat.id

    data = {
        'chat_id': chat_id,
        'type': 'new_duty',

        'name': None,  # 'defaultname',
        'start_time': None,  # datetime.datetime.utcnow(),
        'frequency': None,  # datetime.timedelta(days=1),
        'message': 'JUST DO IT',
        'flatmates': None,  # ['Ed', 'Clemens', 'Linda', 'Basti'],
    }

    infos = [{
        'key': 'name',
        'message': "What's your duty's name?",
        'pre_func': [str],
    }, {
        'key': 'start_time',
        'message': f"When should the duty start (hh:mm dd.mm.yy) (CET/CEST)?",
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
        'message': f"What are your flatmates? (order matters)",
        'pre_func': [pre_find_flatmates],
    }]

    def key_handler(message, current_info, data, infos):
        """

        :param message:
        :param current_info:    dict with infos how the next answer should be processed
        :param data:            dict that should be filled for reminder
        :param infos:           list(dicts) that will be used to get user input (for data)
        :return:
        """
        try:
            value = message.text[1:]
            if value == 'exit':
                raise AbortInput

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

        except Exception as e:
            print(e)
            bot.reply_to(message, 'Message could not be processed - please try again')


        sent_msg = bot.send_message(chat_id, current_info['message']+add_abort_message)
        bot.register_next_step_handler(sent_msg, key_handler, current_info, data, infos)

    current_info = infos.pop(0)
    sent_msg = bot.send_message(chat_id, current_info['message']+add_abort_message)
    bot.register_next_step_handler(sent_msg, key_handler, current_info, data, infos)


# ### helpers

def pre_start_time(start_time):
    start_time = datetime.datetime.strptime(start_time, '%H:%M %d.%m.%y')
    if datetime.datetime.utcnow().date() > start_time.date():
        raise NotImplementedError
    start_time = start_time - datetime.timedelta(hours=2)
    return start_time


def pre_find_flatmates(flatmates_string):
    flatmates_list = re.split(', |,| |/', flatmates_string)
    return flatmates_list
