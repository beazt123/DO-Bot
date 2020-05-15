import datetime as dt
import telegram
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from .typing_action import send_typing_action
from ..constants import ADMIN_USER_PSWD

import boto3
from boto3.dynamodb.conditions import Key, Attr

client = boto3.client('dynamodb')
resource = boto3.resource('dynamodb')

PWDCHECK, ADMIN_ACTIONS = 0, 1
GET_DATE, GET_TIME, GET_NAME, GET_DESC, GET_REMARKS, REMIND_DATE = 3, 4, 5, 6, 7, 8
SELECTED_EVENT, DELETE_EVENT = 9, 10



admin_actions_keyboard = [['Add event'],['List events'],['Nothing']]
admin_selected_event = None

event_date = 0
event_time = 0
event_name = ''
event_description = ''
event_remarks = ''
event_reminder_date = 0





@send_typing_action
def admin_update(update, context):
	uid = update.effective_user['id']
	unm = update.effective_user['username']
	fnm = update.effective_user['first_name']
	lnm = update.effective_user['last_name']

	update.message.reply_text( "Hi. Welcome to the admin interface.")
	update.message.reply_text( "You can schedule/edit/delete event reminders here!")
	update.message.reply_text( "Enter admin password:")
	return PWDCHECK


# PWDCHECK
@send_typing_action
def pwd_check(update, context):
	uid = update.effective_user['id']
	get_pwd = update.effective_message.text
	
	print('date and time below')
	print(dt.datetime.now())

	if get_pwd != ADMIN_USER_PSWD:
		update.message.reply_text( "Wrong password! Exit...")
		return ConversationHandler.END

	elif get_pwd == ADMIN_USER_PSWD:												
		update.message.reply_text( "Welcome admin!")
		update.message.reply_text("What would you like to do?", reply_markup = ReplyKeyboardMarkup(admin_actions_keyboard))
		return ADMIN_ACTIONS


# ADMIN_ACTIONS
@send_typing_action
def admin_actions(update, context):
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	
	if user_response == 'Add event':
		update.message.reply_text("What's the date of the event?\nEnter in the following format DD/MM/YYYY.", reply_markup = ReplyKeyboardRemove())
		return GET_DATE
	
	elif user_response == 'List events':		
		event_mcq = [['Back to main menu']]
		
		# Retrieve all event names and lets the user select
		response = client.scan(TableName = "events_database")
		users = response["Items"] # rows of data including the primary key
		
		for user in users: 
			event_mcq.append([user["event_name"]["S"]])
		
		update.message.reply_text("Alright. Which event would you like to view?", reply_markup = ReplyKeyboardMarkup(event_mcq))
		return SELECTED_EVENT
	
	elif user_response == "Nothing":
		update.message.reply_text( "Aye aye. Have a good day!", reply_markup = ReplyKeyboardRemove())
		return ConversationHandler.END

# SELECTED_EVENT
@send_typing_action
def selected_event(update,context):
	global admin_selected_event
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	
	if user_response == 'Back to main menu':
		update.message.reply_text( "Redirecting you back to main menu", reply_markup = ReplyKeyboardMarkup(admin_actions_keyboard))
		return ADMIN_ACTIONS
	
	admin_selected_event = user_response	

	response = resource.Table("events_database").query(KeyConditionExpression = Key('event_name').eq(user_response))
	# print('response generated')
	# print(type(response))
	# print(response)
	# print('look up')
	
	search = response['Items'][0]
	
	# There should only be 1 item in response
	name = search["event_name"]
	date = search["event_details"]['date']
	time = search["event_details"]['time']
	description = search["event_details"]['description']
	remarks = search["event_details"]['remarks']
	remind = search["event_details"]['remind']
	
	update.message.reply_text("You selected:\n\n*Name*: {}\n*Date*: {}\n*Time*: {}\n*Description*:\n{}\n\n*Remarks*:\n{}\n\n*Date to remind*: {}".format(name,date,time,description,remarks,remind), parse_mode=telegram.ParseMode.MARKDOWN)
	update.message.reply_text("Would you like to do next?",reply_markup=ReplyKeyboardMarkup([['Delete it','Back to main menu']]))
	
	return DELETE_EVENT

# DELETE_EVENT
@send_typing_action
def delete_event(update, context):
	global admin_selected_event
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	
	if user_response == 'Delete it':
	# deleting user information from database
		client.delete_item(
			TableName = "events_database",
			Key = {
			 "event_name": {
							"S": admin_selected_event
							}

			}
			 )
		update.message.reply_text("OK! Your event has been deleted. Redirecting you back to the main menu.", reply_markup=ReplyKeyboardMarkup(admin_actions_keyboard))
	elif user_response == "Back to main menu":
		update.message.reply_text("Ok. Redirecting you back to the main menu.",reply_markup=ReplyKeyboardMarkup(admin_actions_keyboard))
	
	
	return ADMIN_ACTIONS
		

	
		
# GET_DATE
@send_typing_action
def request_date(update, context):
	global event_date
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	day, month, year = user_response.strip().split('/')
	
	# Correct the date
	if int(year) < 100:
		year = int(year) + 2000
	
	# Check date for validity
	try:
		event_date = dt.date(int(year), int(month), int(day))
	except ValueError:
		update.message.reply_text( "Invalid date. Enter the date in the following format DD/MM/YYYY")
		return GET_DATE
	
	update.message.reply_text( "Noted.\nEnter the event time in the format HH.MM")
	return GET_TIME
	
# GET_TIME
@send_typing_action
def request_time(update, context):
	global event_time
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	hour, min = user_response.strip().split('.')
	
	# Check time for validity
	try:
		event_time = dt.time(int(hour),int(min))
	except ValueError:
		update.message.reply_text("Invalid time. Enter the time in the following 24H clock format HH.MM")
		return GET_TIME
	
	update.message.reply_text( "Ok. What's the name of the event?")
	return GET_NAME

# GET_NAME
@send_typing_action
def request_event_name(update, context):
	global event_name
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	
	event_name = user_response
	
	update.message.reply_text( "Got it. Any description for the event to briefly remind subscribers what it is about? Send it to me in 1 long text. Type 'skip' if not applicable.")
	
	return GET_DESC
	
# GET_DESC
@send_typing_action
def request_description(update, context):
	global event_description
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	
	if user_response.lower() != 'skip':
		event_description = user_response
	else:
		event_description = 'N.A'
	update.message.reply_text( "Alrighty. Lastly, any remarks or additional notes? Again pls send it to me in point form. Type 'skip' if not applicable. Press enter for a new line.\nI.e. Remember to bring your umbrella in case it rains, bring your timesheet, etc")
	
	return GET_REMARKS
	
# GET_REMARKS
@send_typing_action
def request_remarks(update, context):
	global event_remarks
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	
	if user_response.lower() != 'skip':
		event_remarks = user_response
	else:
		event_remarks = 'N.A'
	update.message.reply_text( "Almost done! Here is a preview of your reminder.")
	
	# Changed the formatting of the event date and time. Not sure if it works
	long_txt = "Hi there!\nYou got an event reminder!\n*Name*: {}\n*Date*: {}\n*Time*: {}".format(event_name, event_date.strftime('%d/%m/%Y'), event_time.strftime('%I:%M %p'))
	
	if event_description != '':
		long_txt += "\n\n*Description*\n{}".format(event_description)
	
	if event_remarks != '':
		long_txt += "\n\n*Things to note*\n{}".format(event_remarks)
	
	
	update.message.reply_text(long_txt, parse_mode=telegram.ParseMode.MARKDOWN)
	context.bot.send_message(uid, "When would you like to remind the participants? Enter a data in the format DD/MM/YYYY.\nThe reminder will be sent at 12pm on that day.")
	
	return REMIND_DATE

# REMIND_DATE
@send_typing_action
def remind_date(update, context):
	global event_date
	global event_time
	global event_name
	global event_description
	global event_remarks
	global event_reminder_date
	
	uid = update.effective_user['id']
	user_response = update.effective_message.text
	day, month, year = user_response.strip().split('/')
	
	# Correct the date
	if int(year) < 100:
		year = int(year) + 2000
	
	# Check date for validity
	try:
		event_reminder_date = dt.date(int(year), int(month), int(day))
		
		# Check if reminder date is earlier than event date
		if (event_date - event_reminder_date).days < 0:
			update.message.reply_text("Invalid date. Reminder date must be earlier than event date by at least 1 day.")
			return REMIND_DATE
	except ValueError:
		update.message.reply_text("Invalid date. Enter the date in the following format DD/MM/YYYY")
		return REMIND_DATE
	
	# Add the reminder to the events_database
	client.put_item(
	TableName = "events_database", 
	Item = {
		"event_name": {
			"S": event_name
			},
		"event_details":{
			"M": {
				"date":{
					"S": event_date.strftime('%d/%m/%Y')
				}, 
				"time":{
					"S": event_time.strftime('%I:%M %p')
				},
				"description":{
					"S": event_description
				},
				"remarks":{
					"S": event_remarks
				},
				"remind":{
					"S": event_reminder_date.strftime('%d/%m/%Y')
				}
				
			}
		}
	  }  
	)
	
	update.message.reply_text("Woosh! Your reminder has been added!")
	
	# Reset the global variables
	event_date = 0
	event_time = 0
	event_name = ''
	event_description = ''
	event_remarks = ''
	event_reminder_date = 0
	
	update.message.reply_text("What else would you like to do?",reply_markup=ReplyKeyboardMarkup(admin_actions_keyboard))
	return ADMIN_ACTIONS
