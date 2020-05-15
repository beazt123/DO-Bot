from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from utils.googledrive.drive_searching_tool import DriveSearcher

# Set up the credentials for access
SCOPES = 'https://www.googleapis.com/auth/drive'#.metadata'
store = file.Storage('storage.json')		# Change it to your json file that u can obtain after completing the code lab
creds = store.get()

if not creds or creds.invalid: # Change the json file below to the one you downloaded after completing the code lab
    flow = client.flow_from_clientsecrets('client_secret_604344806545-0vglvgq88apra27jhgql9f120vivk0ml.apps.googleusercontent.com.json', SCOPES)
    creds = tools.run_flow(flow, store)


# Everything to do with interacting with drive starts from here
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()), cache_discovery=False)
print("drive instantiated")
searcher = DriveSearcher(DRIVE)

if __name__ == "__main__":
	for i in DRIVE.spreadsheets().values():
		print(i)