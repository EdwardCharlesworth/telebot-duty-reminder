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
    'message': "What's your duty's name?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': False,
    'is_in': False,
    'pre_func': str,
}, {
    'message': f"When should the duty start (hh:mm dd.mm.yy) (CET/CEST)?",
    'data_key': 'start_time',
    'pre_func': pre_start_time,
}, {
    'message': f"In which frequency do you want to be reminded (in days)?",
    'data_key': 'frequency',
    'pre_func': pre_frequency,
}, {
#        'message': f"Please enter a message to ?",
#        'data_key': 'message',
#        'pre_func': str]
#    }, {
    'message': f"What are your members? (order matters)",
    'data_key': 'flatmates',
    'select_type': 'member',
    'send_selection': True,
    'pre_func': pre_find_flatmates,
}, {
    'single_message': 'A new duty was added for your chat!',
}]


delete_duty_input_infos = [{
    'message': "Which duty do you want to delete?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'ALL': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': f"Are you sure you want to delete this duty?",
    'data_key': 'place_holder',
    'pre_func': str,
}, {
    'single_message': 'The duty was deleted!',
}]


list_duty_input_infos = [{
    'message': "Enter a name?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'single_message': """
Every {frequency} days - next time: {start_time} (GMT) - {flatmates} will get notified in this order.
""",
    'insert_info': 'duty',
}]


additional_message_input_text = [{
    'message': "For which duty do you want to extend the message?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': "Please enter a message that will be printed after the member was reminded.",
    'data_key': 'message',
    'pre_func': str,
}, {
    'single_message': """Message was updated""",
}]
