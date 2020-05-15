import json
import logging

from utils.handlers.start_handler import start_handler
from utils.handlers.resources_handler import resources_handler, resources_handler_callback
from utils.handlers.admin_handler import admin_handler, type_of_material
from utils.handlers.briefing_handler import briefing_handler, briefing_handler_material_type
from utils.handlers.feedback_handler import feedback_handler, enter_feedback
from utils.handlers.notif_handler import notif_handler, subscribe_notifications
from utils.handlers.error_handlers import forwardError
from utils.handlers.admin_interface import PWDCHECK, ADMIN_ACTIONS, GET_DATE, GET_TIME, GET_NAME, GET_DESC, GET_REMARKS, REMIND_DATE, SELECTED_EVENT, DELETE_EVENT, admin_update, pwd_check, admin_actions, request_date, request_time, request_event_name, request_description, request_remarks, remind_date, selected_event, delete_event
from utils.handlers.quit_handler import quit
from utils.constants import BOT_TOKEN

from telegram import Update, Bot, ParseMode
from telegram.ext import InlineQueryHandler, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, Dispatcher, Updater

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.ERROR)

# updater = Updater(token=BOT_TOKEN, use_context=True)
# dispatcher = updater.dispatcher
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(CommandHandler('resources', resources_handler))
dispatcher.add_handler(CallbackQueryHandler(resources_handler_callback))
dispatcher.add_handler(ConversationHandler(entry_points=[CommandHandler("admin",admin_handler)],
										   states={
											   1 : [MessageHandler(Filters.text, type_of_material)]
										   },
										   fallbacks=[CommandHandler("quit",quit)]))

dispatcher.add_handler(ConversationHandler(entry_points=[CommandHandler("briefing", briefing_handler)],
										   states={
											   1 : [MessageHandler(Filters.text, briefing_handler_material_type)]
										   },
										   fallbacks=[CommandHandler("quit",quit)]))

dispatcher.add_handler(ConversationHandler(entry_points=[CommandHandler("feedback", feedback_handler)],
										   states={
											   1 : [MessageHandler(Filters.text, enter_feedback)]
										   },
										   fallbacks=[CommandHandler("quit",quit)]))

dispatcher.add_handler(ConversationHandler(entry_points=[CommandHandler("notif", notif_handler)],
										   states={
											   1 : [MessageHandler(Filters.text, subscribe_notifications)]
										   },
										   fallbacks=[CommandHandler("quit",quit)]))

dispatcher.add_handler(ConversationHandler(entry_points=[CommandHandler("damala", admin_update)],
										   states={
											   PWDCHECK : [MessageHandler(Filters.text, pwd_check)],
											   ADMIN_ACTIONS : [MessageHandler(Filters.text, admin_actions)],
											   GET_DATE : [MessageHandler(Filters.text, request_date)],
											   GET_TIME : [MessageHandler(Filters.text, request_time)],
											   GET_NAME : [MessageHandler(Filters.text, request_event_name)],
											   GET_DESC : [MessageHandler(Filters.text, request_description)],
											   GET_REMARKS : [MessageHandler(Filters.text, request_remarks)],
											   REMIND_DATE : [MessageHandler(Filters.text, remind_date)],
											   SELECTED_EVENT: [MessageHandler(Filters.text, selected_event)], 
											   DELETE_EVENT: [MessageHandler(Filters.text, delete_event)]
										   },
										   fallbacks=[CommandHandler("quit",quit)]))


	
def callback(update,context):
	forwardError(context.error)
	logging.exception(context.error)
dispatcher.add_error_handler(callback)

print('5')


# try:
	# updater.start_polling()
	# updater.idle()
# except Exception as e:
	# errMsg(e)
	
def lambda_handler(event, context):
	print('event')
	print(type(event))
	print(event)
	try:
		print('6')
		de_json = Update.de_json(json.loads(event['body']), bot)
		print('7')
		dispatcher.process_update(de_json) # the event object is the update object as a python dict
		print('8')

	except Exception as e:
		print(e)
		return {"statusCode": 500}

	return {"statusCode": 200}