swap_members_input_infos = [{
    'message': "In which duty do you want to swap members?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': f"Please insert the first member name",
    'data_key': 'member1',
    'select_type': 'duty_member',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': f"Please insert the second member name",
    'data_key': 'member2',
    'select_type': 'duty_member',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'single_message': 'Members were switched for one duty!',
}]

exchange_member_input_infos = [{
    'message': "Which member leaves?",
    'data_key': 'old_member',
    'select_type': 'member',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': f"Who's our new member?",
    'data_key': 'new_member',
    'select_type': 'member',
    'send_selection': True,
    'is_in': False,
    'pre_func': str,
}, {
    'single_message': 'Member was exchanged for all duties!',
}]

remove_member_input_infos = [{
    'message': "Which member leaves?",
    'data_key': 'old_member',
    'select_type': 'member',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': f"For what duty?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'ALL': True,
    'is_in': True,
    'pre_func': str,
}, {
    'single_message': 'Member was removed!',
}]


add_member_input_infos = [{
    'message': "Which member?",
    'data_key': 'new_member',
    'select_type': 'member',
    'send_selection': True,
    'is_in': False,
    'pre_func': str,
}, {
    'message': f"For what duty?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'ALL': True,
    'is_in': True,
    'pre_func': str,
}, {
    'single_message': 'Member was added!',
}]


add_duty_member_input_infos = [{
    'message': f"In which duty do you want to add a member?",
    'data_key': 'name',
    'select_type': 'duty',
    'send_selection': True,
    'is_in': True,
    'pre_func': str,
}, {
    'message': "Which member do you want to add?",
    'data_key': 'new_member',
    'select_type': 'duty_member',
    'send_selection': True,
    'is_in': False,
    'pre_func': str,
}, {
    'single_message': 'Member was added!',
}]
