class AbortInput(Exception):
    pass


add_abort_message = "\n'exit' to abort"


def c_greet(bot, message):
    bot.send_message(message.chat.id, 'Hello there!')


### for later use
#from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
#def gen_markup():
#    markup = InlineKeyboardMarkup()
#    markup.row_width = 2
#    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
#                               InlineKeyboardButton("No", callback_data="cb_no"))
#    return markup
