from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from .typing_action import send_typing_action
from ..googledrive.googledrive import searcher

file = searcher

@send_typing_action
def briefing_handler(update, context):
	print("received briefing command")
	custom_keyboard = [['JPM Mentor','Student Mentor'],
						['Exit']]
					   
	reply_markup = ReplyKeyboardMarkup(custom_keyboard)
	
	context.bot.send_message(chat_id=update.message.chat_id, 
					 text="Are you a mentor or a student?", 
					 reply_markup=reply_markup)
	return 1

@send_typing_action
def briefing_handler_material_type(update, context):
	global file
	print("running type of briefing material")
	msg = update.effective_message.text
	print(msg)
	file.clear_q()
	file.is_image(False).n().is_video(False).n().is_trashed(False).n()
	print('file created')
	
	if msg == 'Student Mentor':
		print(msg)
		files = file.is_folder().n().named("SUTD Student Briefing Deck").search()
		print(files)

	elif msg == 'JPM Mentor': 
		print(msg)
		files = file.is_folder().n().named("JPM Mentor Briefing Deck").search()
		print('forms found')
		print(files)

	elif msg == "Exit":
		print(msg)
		update.message.reply_text("Alright. Have a good day.",reply_markup=ReplyKeyboardRemove())
		print('returning')
		
		return -1
	else:
		print("ok lor")
		update.message.reply_text("Sorry, I don't understand that. Mind if you use the special keyboard and try again?",reply_markup=ReplyKeyboardRemove())
		return -1
	reply = ''
	for fil in files:
		reply += fil['name'] + '\n' + fil['webViewLink'] + '\n\n'
	print('reply ready')
	update.message.reply_text("Alright. Here are the materials!\n\n" + reply,reply_markup=ReplyKeyboardRemove())
	print('replied')
	return -1