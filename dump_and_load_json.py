import json
import datetime
import logging

from config import default_dump_path

from reminder.duty_class import DutyObject


def load_duty_dicts(filepath=default_dump_path):
    try:
        with open(filepath) as f:
            duty_dicts = json.load(f)
        return duty_dicts
    except FileNotFoundError:
        return []


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def save_dutys(dutys):
    with open(default_dump_path, "w") as file:
        # ensure that bot is not dumped (not possible)
        dump_str = json.dumps([
            {key: value
             for key, value in duty.__dict__.items() if key != 'bot'}
            for duty in dutys
        ], default=myconverter)
        file.write(dump_str)


def load_dutys(bot):
    databaseName = default_dump_path
    try:
        with open(databaseName,"r") as file:
            duty_dicts = json.load(file)
    except:
        logging.warning("Could not find database ("+databaseName+"). Duty list is empty.")
        duty_dicts = []

    dutys = []
    for duty_dict in duty_dicts:
        duty_dict['start_time'] = datetime.datetime.strptime(duty_dict['start_time'], "%Y-%m-%d %H:%M:%S")
        dutys.append(DutyObject(bot, item=duty_dict))

    return dutys