from dump_and_load_json import load_dutys


def get_default_data(data_type):
    data = {}
    if data_type == 'new_duty':
        data = {'message': 'JUST DO IT'}
    return data


def load_dutys_of_chat(chat_id):
    duty_dicts = load_dutys()

    chat_duty_dicts = []
    for duty_dict in duty_dicts:
        if duty_dict['chat_id'] == chat_id:
            chat_duty_dicts.append(duty_dict)
    return chat_duty_dicts


def get_duty_names(chat_duty_dicts):
    return [duty_dict['name'] for duty_dict in chat_duty_dicts]


def find_duty_in_duty_dicts(duty_name, chat_duty_dicts):
    for duty_dict in chat_duty_dicts:
        if duty_dict['name'] == duty_name:
            return duty_dict
    return False


def find_all_members_of_chat(chat_duty_dicts):
    members = set()
    for duty_dict in chat_duty_dicts:
        members.update(duty_dict['flatmates'])
    return list(members)
