from telegram import InlineQueryResultArticle, InputTextMessageContent

def inline_caps(update, context):
	print("Received upper cmd")
	query = update.inline_query.query
	if not query:
		print('NOT QUERY')
		return
	results = []
	
	# Consolidate results
	results.append(
		InlineQueryResultArticle(
			id=query.upper(),
			title='Upper',
			description='Capitalises your message',
			input_message_content=InputTextMessageContent(query.upper())
		)
	)
	results.append(
		InlineQueryResultArticle(
			id='hello world',
			title='hello-er',
			description='Sends "Hello world" to the chat',
			input_message_content=InputTextMessageContent('hello world')
		)
	)
	# Reply from Bot
	context.bot.answer_inline_query(update.inline_query.id, results)