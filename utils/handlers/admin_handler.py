from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from .typing_action import send_typing_action
from ..googledrive.googledrive import searcher

file = searcher

@send_typing_action
def admin_handler(update, context):
	custom_keyboard = [['Timesheet template'], 
						['Claim forms'], 
					   ['Groupings'],
					   ['Nevermind..']]
					   
	reply_markup = ReplyKeyboardMarkup(custom_keyboard)
	
	context.bot.send_message(chat_id=update.message.chat_id, 
					 text="Please select the document you wish to access", 
					 reply_markup=reply_markup)
	return 1
	
	
@send_typing_action
def type_of_material(update, context):
	global file
	print("running type of material")
	msg = update.effective_message.text
	print(msg)
	file.clear_q()
	file.is_image(False).n().is_video(False).n().is_trashed(False).n()
	print('file created')
	
	if msg == "Timesheet template":
		print(msg)
		files = file.is_folder().n().named("SUTD Student_Timesheet (Monthly Submission)").search()
		print(files)

	elif msg == 'Claim forms': 
		print(msg)
		files = file.is_folder().n().name_contains("SUTD").n().name_contains("Student_Transport").n().name_contains("Claims").search()
		print('forms found')
		print(files)

	elif msg == 'Groupings':
		print(msg)
		files = file.is_folder().n().name_contains("1.").n().name_contains("TSC_Groupings").search()
		print('groups found')
		print(files)

	elif msg == "Nevermind..":
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