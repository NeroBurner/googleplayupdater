# separator used by search.py, categories.py, ...
SEPARATOR = ";"

LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = "130319081" #"38c6523ac43ef9e1"
GOOGLE_LOGIN    = 'tggreatbritain@thinkgaming.com'
GOOGLE_PASSWORD = 'th1nking'
AUTH_TOKEN      = None # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

