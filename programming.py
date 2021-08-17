import telegram


def program_page(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    first_name = update_obj.message.from_user['first_name']
    last_name = update_obj.message.from_user['last_name']
    update_obj.message.reply_text(f"This is programming page for you,{first_name}{last_name}!",
                                  reply_markup=telegram.ReplyKeyboardMarkup(
                                      [['python', 'nodejs', 'Back']],
                                      one_time_keyboard=True)
                                  )




