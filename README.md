# googleplay_updater_cli
Bulk-updater for a folder with apk-files from googleplay

## Configure
Copy the file `config_example.py` or create a new file named `config.py` and fill out your google-account information as well as your `ANDROID_ID`. Your android id can be obtained as descibed in the [googleplay-api](https://github.com/timogilvie/googleplay-api#requirements) project by using the Gtalk Manager on your phone. Or use the java program [android-checkin](https://github.com/nviennot/android-checkin).

## Synopsis
```
usage: gp_update.py [-h] [-c [CONFIG_FILE]] [-v] apk_folder_path

Fetch updates for local apks from GooglePlayStore

positional arguments:
  apk_folder_path       absolute or relative path to folder containing the
                        apks to update

optional arguments:
  -h, --help            show this help message and exit
  -c [CONFIG_FILE], --config_file [CONFIG_FILE]
  -v, --verbose         be more verbose
```

## Dependencies
This section describes the dependencies and the changes done to said dependencies.

### android-sdk-build-tools
Tested with version 23

Available from https://developer.android.com/tools/revisions/build-tools.html

for archlinux-users via AUR https://aur4.archlinux.org/packages/android-sdk-build-tools/

### googleplay-api
Cloned from https://github.com/NeroBurner/googleplay-api which is a fork from https://github.com/timogilvie/googleplay-api

### AsynchronousFilereader
Cloned from https://github.com/soxofaan/asynchronousfilereader

Simple thread based asynchronous file reader for Python.

## Inspiration

Inspired by [GooglePlayDownloader](http://codingteam.net/project/googleplaydownloader) and its 'Search updates for local APK(s)'-button 

## Licence
This project is released under the GPLv3 licence.


