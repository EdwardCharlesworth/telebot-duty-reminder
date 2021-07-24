def c_change_flatmates(bot, queue, message):
    chat_id = message.chat.id

    data = {
        'chat_id': chat_id,
        'type': 'new_duty',

        'name': None,  # 'defaultname',
        'start_time': None,  # datetime.datetime.utcnow(),
        'frequency': None,  # datetime.timedelta(days=1),
        'message': 'JUST DO IT',
        'flatmates': None,  # ['Ed', 'Clemens', 'Linda', 'Basti'],
    }

