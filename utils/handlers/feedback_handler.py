import boto3
from boto3.dynamodb.conditions import Key, Attr
from .typing_action import send_typing_action

client = boto3.client('dynamodb')

@send_typing_action
def feedback_handler(update, context):
	print('received feedback command')
	update.message.reply_text('Feedback? I love to hear your feedback! What do have in mind? Any features you want me to have?')
	return 1

@send_typing_action
def enter_feedback(update,context):
	print('running enter feedback')
	name = update.effective_user['first_name']
	uid = update.effective_user['id']
	suggestion = update.effective_message.text
	update_id = update.update_id
	print('obtained suggestion')
	
	client.put_item(
        TableName = "feedback_database", 
        Item = {
            "sutd_id": {"S": str(update_id)},
            "feedback details":{"M": {
									"user_particulars":{
													"M": {
														"user_first_name": {"S": name},
														"user telegram id": {"N": str(uid)}
														}}, 
									"feedback":{"S": suggestion}
					}
				}
			}
		)
	
	print('closed file')
	update.message.reply_text("Thanks for your feedback. I'll tell my developer about it.")
	print('replied user')
	return -1
