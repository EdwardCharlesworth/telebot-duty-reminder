import requests
import json
import telebot
import datetime


def c_greet(bot, message):
    bot.send_message(message.chat.id, 'Hello there!')


def c_new_duty(bot, queue, message):
    data = {
        'chat_id': message.chat.id,
        'type': 'new_duty',

        'name': None,
        'day': 7,
        'start_time': datetime.datetime.utcnow(),
        'flatmates': ['Ed', 'Clemens', 'Linda', 'Basti'],
        'message': 'Du bist dran',
    }

    def get_user_input(message, function):
        bot.register_next_step_handler(message, function)

    def name_handler(message):
        chat_id = message.chat.id
        # house = get_house(houses, chat_id, bot)
        # bot.register_next_step_handler(sent_msg, name_handler)
        name = message.text
        data['name'] = name

        sent_msg = bot.send_message(chat_id, f"When should {name} start?")
        get_user_input(sent_msg, start_time_handler)

    def start_time_handler(pm):
        weekday = pm.text
        data['start_time'] = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4,
            'Saturday': 5,
            'Sunday': 6,
        }[weekday]
        bot.send_message(pm.chat.id, f"You will be reminded every {weekday}.")

    sent_msg = bot.send_message(message.chat.id, "What's your duty's name?")

    get_user_input(sent_msg, name_handler)  # Next message will call the name_handler function

    queue.put(data)


# ### helpers






### for later use
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#def gen_markup():
#    markup = InlineKeyboardMarkup()
#    markup.row_width = 2
#    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                               InlineKeyboardButton("No", callback_data="cb_no"))
#    return markup
