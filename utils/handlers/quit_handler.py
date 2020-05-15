from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove


def quit(bot, update):
    bot.send_message(uid,"SUCCESSFULLY QUIT...",reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
