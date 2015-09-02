# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import unicode_literals

LANG            = "en_US" # can be en_US, fr_FR, ...
ANDROID_ID      = None # "38c6523ac43ef9e1"
GOOGLE_LOGIN    = None # 'someone@gmail.com'
GOOGLE_PASSWORD = None # 'yourpassword'
AUTH_TOKEN      = None # "yyyyyyyyy"

# force the user to edit this file
if ANDROID_ID == NONE
    or all([each == None for each in [GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN]]):
    raise Exception("config.py not updated")

