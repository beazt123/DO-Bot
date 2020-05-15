class DriveSearcher:
	def __init__(self,drive_obj):
		self.drive = drive_obj
		self.files = self.drive.files()
		self.q = ""
	def search(self,query = None):
		print('getting the query string')
		if query == None:
			query_term = self.q[:-1]
		else:
			query_term = query
		print('query string obtained')
		page_token = None
		a = []
		while True:
			print("searching drive ...")
			response = self.files.list(q = query_term,
										# spaces='drive',
										corpora = 'user',
										fields="*",
										pageToken=page_token
										).execute()
			print('response initiated')
			for file in response.get('files', []):
				# print('file found')
				# print('keys:', file.keys())
				a.append(file)
				print('iterating thru response')
			
			page_token = response.get('nextPageToken', None)
			print('moving on to next page')
			if page_token is None:
				print('breaking')
				break
		
		self.q = ""
		
		return a
			
	def clear_q(self):
		self.q = ""
		
	def n(self):
		self.q += 'and '
		return self
	
	def o(self):
		self.q += 'or '
		return self
		
	def q(self):
		return self.q
	
	def named(self, name):
		self.q += "name = '" + name + "' "
		return self
		
	def name_contains(self, *args):
		for word in args:
			self.q += "name contains '" + word + "' and "
		self.q = self.q[:-4]
		return self
	 
	def is_folder(self,really_is_folder = True):
		if really_is_folder:
			self.q += "mimeType = 'application/vnd.google-apps.folder' "
		else:
			self.q += "mimeType != 'application/vnd.google-apps.folder' "
		return self
	
	def is_trashed(self,really_is_trashed = True):
		if really_is_trashed:
			self.q += "trashed = true "
		else:
			self.q += "trashed = false "
		return self
		
	def text_has(self, *args, really_contains_those_words = True):
		if really_contains_those_words:
			for word in args:
				self.q += "fullText contains '" + word + "' and "
			self.q = self.q[:-4]
		else:
			for word in args:
				self.q += "not fullText contains '" + word + "' and "
			self.q = self.q[:-4]
		return self
		
	def shared_with_me(self):
		self.q += "sharedWithMe "
		return self
	
	def is_image(self,really_is_image = True):
		if really_is_image:
			self.q += "mimeType contains 'image/' "
		else:
			self.q += "not mimeType contains 'image/' "
		return self
	
	def is_video(self,really_is_video = True):
		if really_is_video:
			self.q += "mimeType contains 'video/' "
		else:
			self.q += "not mimeType contains 'video/' "
		return self
		
	def is_pdf(self):
		self.q += "mimeType = 'application/pdf' "
		
