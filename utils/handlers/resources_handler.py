from .typing_action import send_typing_action
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


# When user requests for links to workshop ppt, below is the reply
request_workshop_reply = \
'''Select the workshop you have in mind...'''
# After the user selects a workshop, the bot sends them the link along with the text below
link_workshop_reply = \
'''We have found the documents, check them out below!'''


@send_typing_action	
def resources_handler(update,context):
	print('received resources command')
	
	keyboard = [[InlineKeyboardButton("Student Handbook", callback_data='handbook')],
                [InlineKeyboardButton("Workshop Materials", callback_data='workshop')]]
	reply_markup = InlineKeyboardMarkup(keyboard)
	update.message.reply_text(request_workshop_reply, reply_markup=reply_markup)
	print("replied to resources command")

# This is a callback function and not a handler
@send_typing_action
def resources_handler_callback(update, context):
	print('received resources_callback command')
	query = update.callback_query
	print('received user query')
	
	if query.data == "handbook":
		print('received handbook cmd')
		file_link = 'Student Handbook' + '\n' + 'https://drive.google.com/file/d/1x2vJl168LrRmDEMGe6GBO2z-hPaqTmuw/view?usp=sharing' + '\n\n'
		print(file_link)
		
	else:
		print('received workshop materials cmd')
		file_link = 'Workshop Materials' + '\n' + 'https://drive.google.com/drive/folders/1W2H8Za4wYkOK-BrVZm93jn0VYdIK6IbA' + '\n\n'
		print('file: workshop')
		print('msg sent')
	
	query.edit_message_text(text=link_workshop_reply + '\n\n' + file_link)
	print('replied resources_callback')