import telebot
from typing import List


add_abort_message = "\n'exit' to abort"


def check_for_exit(bot):
    def inner_check_for_exit(func):
        def wrapper(*args, **kwargs):
            message = args[0]
            value = message.text[1:]
            if value == 'exit':
                bot.send_message(message.chat.id, 'Command was aborted')
                return
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

    data = {
        'chat_id': chat_id,
        'type': data_type,
    }

    @check_for_exit(bot)
    def data_key_handler(inner_message, current_info, data, infos):
        """

        :param inner_message:
        :param current_info:    dict with infos how the next answer should be processed
        :param data:            dict that should be filled for reminder_temp
        :param infos:           list(dicts) that will be used to get user input (for data)
        :return:
        """
        try:
            value = inner_message.text[1:]

            # apply individual preprocessing functions to input value
            data[current_info['data_key']] = current_info['pre_func'](value)

            try:
                # get next info
                next_info = infos.pop(0)
            except IndexError:
                # end with sending data to reminder_temp
                queue.put(data)
                return

        except Exception as e:
            print(e)
            bot.reply_to(inner_message, 'Message could not be processed - please try again')
            return

        sent_inner_msg = bot.send_message(chat_id, next_info['message']+add_abort_message)
        bot.register_next_step_handler(sent_inner_msg, data_key_handler, next_info, data, infos)

    current_info = infos.pop(0)
    sent_msg = bot.send_message(chat_id, current_info['message']+add_abort_message)
    bot.register_next_step_handler(sent_msg, data_key_handler, current_info, data, infos)


### for later use
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#def gen_markup():
#    markup = InlineKeyboardMarkup()
#    markup.row_width = 2
#    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                               InlineKeyboardButton("No", callback_data="cb_no"))
#    return markup
