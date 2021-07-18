import json
import telebot
import sched
import datetime
import time

from house import House



def load_houses():
    try:
        with open('houses_dump.json', 'r') as fp:
            houses = json.load(fp, indent=4)
    except Exception:
        houses = {}

    return houses


def get_house(houses, chat_id, bot=None):
    try:
        house = houses[chat_id]
    except KeyError:
        house = House(chat_id)
        houses[chat_id] = house

        if bot is not None:
           bot.send_message(chat_id, 'A new house was created.')

    return house
