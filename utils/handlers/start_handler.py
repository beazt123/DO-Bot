from .typing_action import send_typing_action
from telegram import ReplyKeyboardRemove

welcome = \
''' 
I’m your very own design companion! How can I help you today?

/admin [schools challenge] 
Admin documents I.e. Timesheet, claim forms, groupings

/briefing [schools challenge] 
Click here to find out more about the schools challenge

/resources
Click here to access the workshop materials & handbook

/feedback
Click here to tell me what features you want next!
(Only works if you pm me!)

/notif
Missing our workshops? Fret not! Auto reminder feature is here to save the day!
'''

@send_typing_action
def start_handler(update, context):	
	print('received start command')
	reply_welcome = 'Hi {}!\n'.format(update.effective_user['first_name']) + welcome
	update.message.reply_text(reply_welcome, reply_markup=ReplyKeyboardRemove())
	print('replied to start command')