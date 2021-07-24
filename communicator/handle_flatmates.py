swap_members_input_infos = [{
    'data_key': 'name',
    'message': "In which duty do you want to swap members?",
    'pick_from': 'duty',
    'pre_func': str,
}, {
    'data_key': 'member1',
    'message': f"Please insert the first member name",
    'pick_from': 'members',
    'pre_func': str,
}, {
    'data_key': 'member1',
    'message': f"Please insert the second member name",
    'pick_from': 'members',
    'pre_func': str,
}]

exchange_members_input_infos = [{
    'data_key': 'name',
    'message': "Which flatmate leaves?",
    'pre_func': str,
}, {
    'data_key': 'flatmates',
    'message': f"Who's the ",
    'pre_func': str,
}]
