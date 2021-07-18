def communicate():
    pass



import requests
import json
import telebot

from house import Duty
from initialize import *


houses = load_houses



@bot.message_handler(commands=['save_houses'])
def save_houses(message):
    with open('houses_dump.json', 'w') as fp:
        json.dump([house.get_dict_representation() for house in houses.values()], fp, indent=4)
    bot.reply_to(message, 'houses were saved')


@bot.message_handler(commands=['greet'])
def greet(message):

    bot.send_message(message.chat.id, 'Hello there! '+str(message.chat.id))

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup



def get_user_input(message, function):
    bot.register_next_step_handler(message, function)




@bot.message_handler(commands=['new_duty'])
def new_duty(message):
    sent_msg = bot.send_message(message.chat.id, "What's your duty's name?")

    get_user_input(sent_msg, name_handler)  #Next message will call the name_handler function


def name_handler(message):
    chat_id = message.chat.id
    # house = get_house(houses, chat_id, bot)
    # bot.register_next_step_handler(sent_msg, name_handler)
    name = message.text[1:]


    sent_msg = bot.send_message(chat_id, f"Your name is {name}. how old are you?")
    bot.register_next_step_handler(sent_msg, age_handler, name) #Next message will call the age_handler function

def weekday_handler(pm, name):
    age = pm.text
    bot.send_message(pm.chat.id, f"Your name is {name}, and your age is {age}.")




def reminder():
    while(True):
        time.sleep(10)
        # update schedule

        # read

        # sned
        bot.send_message(chat_id, f"i waited {seconds} seconds")


@bot.message_handler(commands=['wait'])
def set_duty(message):
    bot._exec_task(reminder)




def action():
    sent_msg = bot.send_message(chat_id, "What's your duty's name?")
    print('asd')


bot.polling()


print('end')