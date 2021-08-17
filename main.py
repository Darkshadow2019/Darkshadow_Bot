import telegram
import telegram.ext
import re
from random import randint
import logging

import linux
import programming
import windows

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# The API Key we received for our bot
API_KEY = "1947176006:AAG-lpzOmldlfD1ARZsLV6DRwgtS7Fi_8Qs"

# Create an updater object with our API Key
updater = telegram.ext.Updater(API_KEY)

# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher

# Our states, as integers
WELCOME = 0
QUESTION = 1
CANCEL = 2
CORRECT = 3
WIN_SUB = 4
LINUX_SUB = 5
PROGRAMMING = 6
KEYBOARD_R = 7


# The entry function
def start(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello there,\nWhat are looking for?🔎"
                                  "\nor question test?",
                                  reply_markup=telegram.ReplyKeyboardMarkup(
                                      [['Yes', 'No', 'Cancel'], ['Windows', 'Linux'], ['Programming']],
                                      one_time_keyboard=True)
                                  )
    # go to the WELCOME state
    return WELCOME


# helper function, generates new numbers and sends the question
def randomize_numbers(update_obj, context):
    # store the numbers in the context
    context.user_data['rand_x'], context.user_data['rand_y'] = randint(0, 1000), randint(0, 1000)
    # send the question
    update_obj.message.reply_text(f"Calculate {context.user_data['rand_x']}+{context.user_data['rand_y']}")


# in the WELCOME state, check if the user wants to answer a question
def welcome(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        # send question, and go to the QUESTION state
        randomize_numbers(update_obj, context)
        return QUESTION

    if update_obj.message.text.lower() in ['windows', 'w']:
        # go to the Windows state
        go_to_win(update_obj, context)

    if update_obj.message.text.lower() in ['wintools']:
        windows.win_tools(update_obj, context)
        return go_to_win(update_obj, context)

    if update_obj.message.text.lower() in ['winpdfs']:
        windows.win_pdfs(update_obj, context)
        return go_to_win(update_obj, context)

    if update_obj.message.text.lower() in ['linux']:
        go_to_linux(update_obj, context)

    if update_obj.message.text.lower() in ['programming']:
        # go to the programming state
        go_to_programming(update_obj, context)

    if update_obj.message.text.lower() in ['back', 'b']:
        # back to main page
        repair_kb(update_obj, context)

    if update_obj.message.text.lower() in ['cancel']:
        return CANCEL

    else:
        # go to the CANCEL state
        return WELCOME


# in the QUESTION state
def question(update_obj, context):
    # expected solution
    solution = int(context.user_data['rand_x']) + int(context.user_data['rand_y'])
    # check if the solution was correct
    if solution == int(update_obj.message.text):
        # correct answer, ask the user if he found tutorial helpful, and go to the CORRECT state
        update_obj.message.reply_text("Correct answer!")
        update_obj.message.reply_text("Was this tutorial helpful to you?")
        return CORRECT
    else:
        # wrong answer, reply, send a new question, and loop on the QUESTION state
        update_obj.message.reply_text("Wrong answer :'(")
        # send another random numbers calculation
        randomize_numbers(update_obj, context)
        return QUESTION


# in the CORRECT state
def correct(update_obj, context):
    if update_obj.message.text.lower() in ['yes', 'y']:
        update_obj.message.reply_text("Glad it was useful! ^^")
    else:
        update_obj.message.reply_text("You must be a programming wizard already!")
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    last_name = update_obj.message.from_user['last_name']
    update_obj.message.reply_text(f"See you {first_name}{last_name}!, bye")
    update_obj.message.reply_text("😘")
    return WELCOME


def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    last_name = update_obj.message.from_user['last_name']
    update_obj.message.reply_text(
        f"Okay, See you later, {first_name}{last_name}\nByeBye!!! 🥰",
        reply_markup=telegram.ReplyKeyboardRemove()
    )
    update_obj.message.reply_text("😘")
    return telegram.ext.ConversationHandler.END


# Windows courses
def go_to_win(update_obj, context):
    windows.win_page(update_obj, context)


# Linux courses
def go_to_linux(update_obj, context):
    linux.linux_page(update_obj, context)


# Programming courses
def go_to_programming(update_obj, context):
    programming.program_page(update_obj, context)


# Repair Keyboard
def repair_kb(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    update_obj.message.reply_text("Hello there,\nWhat are looking for?🔎"
                                  "\nor question test?",
                                  reply_markup=telegram.ReplyKeyboardMarkup(
                                      [['Yes', 'No', 'Cancel'], ['Windows', 'Linux'], ['Programming']],
                                      one_time_keyboard=True)
                                  )
    # go to the WELCOME state
    return WELCOME


if __name__ == '__main__':
    # a regular expression that matches yes or no
    yes_no_regex = re.compile(r'^(yes|no|y|n|windows|wintools|winpdfs|linux|programming|back|cancel)$', re.IGNORECASE)

    # Create our ConversationHandler, with only one state
    handler = telegram.ext.ConversationHandler(
        entry_points=[telegram.ext.CommandHandler('start', start)],
        states={
            WELCOME: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), welcome)],
            QUESTION: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(r'^\d+$'), question)],
            CANCEL: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), cancel)],
            CORRECT: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), correct)],
            WIN_SUB: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), go_to_win)],
            LINUX_SUB: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), go_to_linux)],
            PROGRAMMING: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), go_to_programming)],
            KEYBOARD_R: [telegram.ext.MessageHandler(telegram.ext.Filters.regex(yes_no_regex), repair_kb)]
        },
        fallbacks=[telegram.ext.CommandHandler('cancel', cancel)],
    )

    # add the handler to the dispatcher
    dispatcher.add_handler(handler)

    # start polling for updates from Telegram
    updater.start_polling()
    # block until a signal (like one sent by CTRL+C) is sent
    updater.idle()
