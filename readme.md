# Design Odyssey Telegram Chatbot
---
This is a Telegram chatbot developed to assist in SUTD Design Odyssey's educational programmes. It features semi-automated workshop reminnders and also hosts important workshop information.

## Motivation
---
This project saw an opportunity space in the mobile platform as a place to communicate with the students, as emails and posters tend not to capture the attention of the students.

## API Reference
---
Language: [Python Release Python 3.7.3 \| Python.org](https://www.python.org/downloads/release/python-373/)

Python Telegram API: [Python Telegram](https://python-telegram-bot.readthedocs.io/en/stable/)

Telegram API: [Telegram Bot API](https://core.telegram.org/bots/api)

## Setup
---
The following python libraries are used:
- python telegram
- pytz
- googleapiclient

Note that this set of source code is tailored to be used on [AWS Servers](https://ap-southeast-1.console.aws.amazon.com/console/home?region=ap-southeast-1) (Amazon Web Services).

#### Setting up a new python environment
In case you don't have the python library to help you create the virtual environment, run the following command
```
pip install virtualenv
```
Create your virtual environment. Choose any name for your virtual environment.
```bash
virtualenv <name of virtual environment>
```
Activate your virtual environment.
For mac/linux users,
```bash
source <name of virtual environment>/bin/activate
```
For windows users,
```bash
source <name of virtual environment>/Scripts/activate.bat
```

Now, on the left of the current working directory, where you type your command, there should be the name of virtual environment encapsulated in brackets, something like,
```bash
(teleEnv) D:\Desktop\SUTD\5th rows\DO\DO EXCO\DO Bot\teleEnv\Scripts>  
```
Now you're ready to install the python dependency libraries stated above into the current virtual environment. 
```bash
pip install pytz
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install python-telegram-bot
```
You may observe in the source codes that another library named "boto3" is also imported. That library is part of AWS runtime libraries so it will be included in the runtime environment when you run your code on AWS servers.


#### Setting up your Google API key
You need to set up the api key before using python to access your google drive. Set up your own Python google API key by following the instructions in the link: [Python Quickstart  \|  Google Docs API  |  Google Developers](https://developers.google.com/docs/api/quickstart/python)

#### [Organising the files before use](https://www.youtube.com/watch?v=_REQzvXnEz8)
1) Move all the files into the "site packages" folder.
2) ZIP up the contents of the folder.

!!! caution Caution
For Step 2, be sure to zip the contents inside the folder and not the folder itself
!!!

For actual use, upload the zip file into an AWS lambda function


## HOTO
---
- Google api client credentials
- Bot API key(optional)
- AWS lambda account