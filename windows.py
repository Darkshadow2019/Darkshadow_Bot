import telegram


def win_page(update_obj, context):
    # send the question, and show the keyboard markup (suggested answers)
    first_name = update_obj.message.from_user['first_name']
    last_name = update_obj.message.from_user['last_name']
    update_obj.message.reply_text(f"Windows page for you,{first_name}{last_name}!",
                                  reply_markup=telegram.ReplyKeyboardMarkup(
                                      [['WinPDFs', 'WinTools', 'Back']],
                                      one_time_keyboard=True)
                                  )


def win_tools(update_obj, context):
    # windows tools
    update_obj.message.reply_text("1).Activator:"
                                  "\n2.WSL"
                                  "\3.Other")


def win_pdfs(update_obj, context):
    update_obj.message.reply_text("1).Install Guide:"
                                  "\n2).Repair HDD"
                                  "\n3).Repair RAM")
