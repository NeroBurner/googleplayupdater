
LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = None # "38c6523ac43ef9e1"
GOOGLE_LOGIN    = None # 'someone@gmail.com'
GOOGLE_PASSWORD = None # 'yourpassword'
AUTH_TOKEN      = None # "yyyyyyyyy"

# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

