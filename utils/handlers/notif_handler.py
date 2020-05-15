import boto3
from boto3.dynamodb.conditions import Key, Attr

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from .typing_action import send_typing_action


client = boto3.client('dynamodb')


@send_typing_action
def notif_handler(update, context):
	print("Received notif cmd")	
	custom_keyboard = [['Count me in!','Stop disturbing me.']]
					   
	reply_markup = ReplyKeyboardMarkup(custom_keyboard)
	
	context.bot.send_message(chat_id=update.message.chat_id, 
							text='Would you like to subscribe to our auto reminder feature? It\'ll send you messages before every workshop so that you don\'t forget to come!', 
							reply_markup=reply_markup)
	print('waiting for user response for notifications')
	return 1

@send_typing_action
def subscribe_notifications(update,context):
	global client
	print('received notif answer from user')
	answer = update.effective_message.text
	user_id = update.effective_user.id
	user_first_name = update.effective_user.first_name
	update_id = update.update_id
	
	if answer == 'Count me in!':
		# Append name & ID to client database
		client.put_item(
        TableName = "users_database", 
        Item = {
            "user_id": {
                "N": str(user_id)
                },
            "user_information":{
                "M": {
                    "user_first_name":{
                        "S": user_first_name
                    }, 
                    "update_id":{
                        "N": str(update_id)
                    }
                }
            }
          }  
		)
		print('[Received user particulars]:\t\t Message Update ID:\t{} User: {}\t\t\t User ID: {}'.format(update_id,user_first_name,user_id))
		
		# retrieve user_id from database
		response = client.scan(TableName = "users_database")
		users = response["Items"]
		for user in users: 
			retrieved_user_id = user["user_id"]["N"]
			print(retrieved_user_id)
		update.message.reply_text('Ok. I\'ve noted your name({}) and id({}). Stay tuned for updates!'.format(user_first_name,user_id),reply_markup=ReplyKeyboardRemove())
	
	elif answer == 'Stop disturbing me.':
		# deleting user information from database
		client.delete_item(
			TableName = "users_database",
			Key = {
			 "user_id": {
							"N": str(user_id)
							}

			}
			 )
		
		update.message.reply_text("Alright then! You've successfully unsubscribed from our notifications. But do keep in touch with us!",reply_markup=ReplyKeyboardRemove())
	
	return -1
	








