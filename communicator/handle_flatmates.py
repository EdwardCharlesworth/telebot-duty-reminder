swap_members_input_infos = [{
    'data_key': 'name',
    'message': "In which duty do you want to swap members?",
    'pick_from': 'duty',
    'pre_func': str,
}, {
    'data_key': 'member1',
    'message': f"Please insert the first member name",
    'pick_from': 'duty_members',
    'pre_func': str,
}, {
    'data_key': 'member2',
    'message': f"Please insert the second member name",
    'pick_from': 'duty_members',
    'pre_func': str,
}, {
    'single_message': 'Flatmates were switched for one duty!',
}]

exchange_members_input_infos = [{
    'data_key': 'old_member',
    'message': "Which flatmate leaves?",
    'pick_from': 'members',
    'pre_func': str,
}, {
    'data_key': 'new_member',
    'message': f"Who's our new flatmate?",
    'pre_func': str,
}, {
    'single_message': 'Flatmates were exchanged for all duties!',
}]
