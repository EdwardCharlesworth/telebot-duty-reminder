import telebot
import json
from typing import List
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import add_abort_message, no, yes

from communicator.helper import get_default_data, load_dutys_of_chat, \
    find_duty_in_duty_dicts, find_all_members_of_chat, get_duty_names


class InputError(Exception):
    pass


class AlreadyExists(InputError):
    pass


class IsNotPresent(InputError):
    pass


def get_input_from_call_or_message(call_or_msg):
    if isinstance(call_or_msg, telebot.types.CallbackQuery):
        value = call_or_msg.data
    elif isinstance(call_or_msg, telebot.types.Message):
        value = call_or_msg.text
        if value.startswith('/'):
            value = value[1:]
    else:
        raise InputError
    return value


def gen_markup(options: List[str], row_width=3):
    markup = InlineKeyboardMarkup(row_width=row_width)
    keyboard_buttons = []
    for option in options:
        keyboard_buttons.append(InlineKeyboardButton(option, callback_data=option))
    markup.add(*keyboard_buttons)
    return markup


def check_for_exit(bot):
    def inner_check_for_exit(func):
        def wrapper(*args, **kwargs):
            message = args[0]
            value = get_input_from_call_or_message(message)
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

    data = get_default_data(data_type)
    data.update({
        'chat_id': chat_id,
        'type': data_type,
    })

    chat_duty_dicts = []
    for info in infos:
        if 'select_type' in info.keys():
            chat_duty_dicts = load_dutys_of_chat(chat_id)
            break

    @check_for_exit(bot)
    def data_key_handler(inner_message, current_info, data, infos, first_message=False,
                         validation_list=None, is_in=None):
        """

        :param inner_message:
        :param current_info:    dict with infos how the next answer should be processed
        :param data:            dict that should be filled for reminder
        :param infos:           list(dicts) that will be used to get user input (for data)
        :param first_message:   if False: will check for input in inner_message
        :param validation_list: list of (not-)possible inputs
        :param is_in:           if True: error if user input is not in validation_list
                                if False: error if user input is in validation_list
        :return:
        """
        if not first_message:
            try:
                # get input
                value = get_input_from_call_or_message(inner_message)
                # apply individual preprocessing functions to input value
                post_value = current_info['pre_func'](value)
                data[current_info['data_key']] = post_value

                # validate input
                if is_in and post_value not in validation_list:
                    raise IsNotPresent(f'{post_value} is not in {validation_list}')
                elif not is_in and post_value in validation_list:
                    raise AlreadyExists(f'{post_value} is in {validation_list}')

            except Exception as e:
                print(e)
                if not isinstance(inner_message, telebot.types.CallbackQuery):
                    if isinstance(e, IsNotPresent):
                        sent_inner_msg = bot.reply_to(inner_message, 'name does not exist - please try again')
                    elif isinstance(e, AlreadyExists):
                        sent_inner_msg = bot.reply_to(inner_message, 'name already exists - please try again')
                    else:
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

                    # get message
                    raw_message = next_info['single_message']
                    if not yes == data.get('confirm', yes) and 'single_abort_message' in next_info.keys():
                        raw_message = next_info['single_abort_message']

                    # get format_dict for message
                    format_dict = {}
                    if next_info.get('insert_info', False):
                        format_dict = find_duty_in_duty_dicts(data['name'], chat_duty_dicts)

                    _ = bot.send_message(chat_id, raw_message.format(**format_dict))

                    if not yes == data.get('confirm', yes):
                        return

                    next_info = infos.pop(0)

            except IndexError:
                # end with sending data to reminder
                if data['type'] != 'NOTHING':
                    queue.put(data)
                return

        else:
            next_info = current_info

        send_selection = next_info.get('send_selection', None)
        is_in = next_info.get('is_in', None)
        keyboard_input = True if send_selection and is_in else False
        select_type = next_info.get('select_type', None)
        all_selections = next_info.get('ALL', None)

        select_list = []
        pre_list_message_text = ''
        if select_type:
            if select_type == 'duty':
                # get all duties
                select_list = get_duty_names(chat_duty_dicts)
                pre_list_message_text = '\nCurrent duties:'
            elif select_type == 'duty_member':
                # get members of one duty
                select_list = find_duty_in_duty_dicts(data['name'], chat_duty_dicts)['flatmates']
                pre_list_message_text = '\nCurrent duty members:'
            elif select_type == 'member':
                # get all members
                select_list = find_all_members_of_chat(chat_duty_dicts)
                pre_list_message_text = '\nAll members:'
            else:
                raise NotImplementedError

        # build message text
        message_text = next_info['message']+add_abort_message
        if send_selection and len(select_list) > 0:
            message_text += '\n' + pre_list_message_text
            if not keyboard_input:
                for value in select_list:
                    message_text += '\n'
                    message_text += str(value)
                if all_selections:
                    message_text += '\n"ALL" for all'

        validation_list = next_info.get('options', select_list)
        if all_selections:
            validation_list.append('ALL')

        @bot.callback_query_handler(func=lambda call: call.message.chat.id == chat_id, chat_id=chat_id)
        def callback_query(call):
            data_key_handler(call, next_info, data, infos,
                             validation_list=validation_list, is_in=is_in)
            bot.answer_callback_query(call.id, call.data)

        if keyboard_input:
            bot.send_message(chat_id, message_text, reply_markup=gen_markup(validation_list))
        else:
            sent_inner_msg = bot.send_message(chat_id, message_text)
            bot.register_next_step_handler(sent_inner_msg, data_key_handler, next_info, data, infos,
                                           validation_list=validation_list, is_in=is_in)

    current_info = infos.pop(0)
    data_key_handler(message, current_info, data, infos, first_message=True)
