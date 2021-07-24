import datetime
import re


def pre_start_time(start_time):
    start_time = datetime.datetime.strptime(start_time, '%H:%M %d.%m.%y')
    if datetime.datetime.utcnow().date() > start_time.date():
        raise NotImplementedError
    start_time = start_time - datetime.timedelta(hours=2)
    return start_time


def pre_find_flatmates(flatmates_string):
    flatmates_list = re.split(', |,| |/', flatmates_string)
    return flatmates_list


def pre_frequency(day_string):
    return datetime.timedelta(int(day_string))


# 'name': None,  # 'defaultname',
# 'start_time': None,  # datetime.datetime.utcnow(),
# 'frequency': None,  # datetime.timedelta(days=1),
# 'message': 'JUST DO IT',
# 'flatmates': None,  # ['Ed', 'Clemens', 'Linda', 'Basti'],


new_duty_input_infos = [{
    'data_key': 'name',
    'message': "What's your duty's name?",
    'pick_not_from': 'duty',
    'pre_func': str,
}, {
    'data_key': 'start_time',
    'message': f"When should the duty start (hh:mm dd.mm.yy) (CET/CEST)?",
    'pre_func': pre_start_time,
}, {
    'data_key': 'frequency',
    'message': f"In which frequency do you want to be reminded (in days)?",
    'pre_func': pre_frequency,
}, {
#        'data_key': 'message',
#        'message': f"Please enter a message to ?",
#        'pre_func': str]
#    }, {
    'data_key': 'flatmates',
    'message': f"What are your flatmates? (order matters)",
    'pre_func': pre_find_flatmates,
}, {
    'single_message': 'A new duty was added for your chat!',
}]

