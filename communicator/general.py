import telebot
import json
from typing import List

from config import maximum_input_trys

from communicator.helper import get_default_data, load_dutys_of_chat, \
    find_duty_in_duty_dicts, find_all_members_of_chat, get_duty_names


add_abort_message = "\n'exit' to abort"


class InputError(Exception):
    pass


def check_for_exit(bot):
    def inner_check_for_exit(func):
        def wrapper(*args, **kwargs):
            message = args[0]
            value = message.text[1:]
            if value == 'exit':
                bot.send_message(message.chat.id, 'Command was aborted')
                return
            else:
                func(*args, **kwargs)
        return wrapper
    return inner_check_for_exit


def c_greet(bot, message):
    bot.send_message(message.chat.id, 'Hello there!')


def get_user_input(bot, queue, message, infos: List[dict], data_type: str = None):
    """

    :param bot:
    :param queue:
    :param message:
    :param infos:       list of dicts with the following keys: 'data_key', 'message', 'pre_func'
    :param data_type:
    :return:
    """
    chat_id = message.chat.id
    pick_from_duty_name = None

    data = get_default_data(data_type)
    data.update({
        'chat_id': chat_id,
        'type': data_type,
    })

    chat_duty_dicts = []
    for info in infos:
        if 'pick_from' in info.keys() \
                or 'pick_not_from' in info.keys():
            chat_duty_dicts = load_dutys_of_chat(chat_id)
            break

    @check_for_exit(bot)
    def data_key_handler(inner_message, current_info, data, infos, first_message=False,
                         validation_list=None, is_in=None):
        """

        :param inner_message:
        :param current_info:    dict with infos how the next answer should be processed
        :param data:            dict that should be filled for reminder_temp
        :param infos:           list(dicts) that will be used to get user input (for data)
        :return:
        """
        if not first_message:
            try:
                # get input
                value = inner_message.text[1:]
                # apply individual preprocessing functions to input value
                post_value = current_info['pre_func'](value)
                data[current_info['data_key']] = post_value

                # validate input
                if is_in and post_value not in validation_list:
                    raise InputError(f'{post_value} is not in {validation_list}')
                elif not is_in and post_value in validation_list:
                    raise InputError(f'{post_value} is in {validation_list}')

            except Exception as e:
                print(e)
                sent_inner_msg = bot.reply_to(inner_message, 'Message could not be processed - please try again')
                bot.register_next_step_handler(sent_inner_msg, data_key_handler, current_info, data, infos,
                                               first_message=first_message, validation_list=validation_list,
                                               is_in=is_in)
                return

            # get next info
            try:
                # get next info
                next_info = infos.pop(0)
                if 'single_message' in next_info.keys():
                    _ = bot.send_message(chat_id, next_info['single_message'])
                    next_info = infos.pop(0)
            except IndexError:
                # end with sending data to reminder_temp
                queue.put(data)
                return

        else:
            next_info = current_info

        send_selection = None
        is_in = None
        pick_type = None

        if 'pick_from' in next_info.keys():
            # prepare output of list-like information about current duties
            send_selection = True
            is_in = True
            pick_type = next_info['pick_from']

        elif 'pick_not_from' in next_info.keys():
            # prepare checking for existing objects
            send_selection = False
            is_in = False
            pick_type = next_info['pick_not_from']

        if pick_type:
            if pick_type == 'duty':
                # get all duties
                pick_from_list = get_duty_names(chat_duty_dicts)
            elif pick_type == 'duty_members':
                # get members of one duty
                pick_from_list = find_duty_in_duty_dicts(pick_from_duty_name, chat_duty_dicts)['flatmates']
            elif pick_type == 'members':
                # get all members
                pick_from_list = find_all_members_of_chat(chat_duty_dicts)
            else:
                raise NotImplementedError

        # build message text
        message_text = next_info['message']+add_abort_message
        pick_from_list = []
        if send_selection:
            for value in pick_from_list:
                message_text += '\n'
                message_text += str(value)

        sent_inner_msg = bot.send_message(chat_id, message_text)
        bot.register_next_step_handler(sent_inner_msg, data_key_handler, next_info, data, infos,
                                       validation_list=pick_from_list, is_in=is_in)

    current_info = infos.pop(0)
    data_key_handler(message, current_info, data, infos, first_message=True)


### for later use
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#def gen_markup():
#    markup = InlineKeyboardMarkup()
#    markup.row_width = 2
#    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                               InlineKeyboardButton("No", callback_data="cb_no"))
#    return markup
