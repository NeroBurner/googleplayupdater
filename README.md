# googleplayupdater
Bulk-updater for a folder with apk-files from googleplay

## Configure
Copy the file `config_example.py` or create a new file named `config.py` and fill out your google-account information as well as your `ANDROID_ID`. Your android id can be obtained as descibed in the [googleplay-api](https://github.com/NeroBurner/googleplay-api#requirements) project by using the Gtalk Manager on your phone. Or use the java program [android-checkin](https://github.com/nviennot/android-checkin).

## Synopsis
```
usage: googleplayupdater [-h] [-c [CONFIG_FILE]] [-v] apk_folder_path

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
* [Python 2.7+ or Python 3.4+](http://www.python.org)
* [Protocol Buffers](http://code.google.com/p/protobuf/) (for googleplay-api)
* [android-sdk-build-tools](https://developer.android.com/tools/revisions/build-tools.html)
  (tested with version 23, for archlinux-users via [AUR](https://aur4.archlinux.org/packages/android-sdk-build-tools/))

## Installation
To install download/clone the repository, change into the downloaded directory and execute:
```
python setup.py install
```

### Python 3
googleplay-api depends on google's protobuf. Only versions greater than 3.0 have support for Python 3. Unfortunately these versions are still in alpha and must be installed manually.
For Arch-linux the package [python-protobuf](https://aur4.archlinux.org/packages/python-protobuf/) is available in the AUR. Otherwise [protobuf-3.0.0a3](https://pypi.python.org/pypi/protobuf/3.0.0a3) can be installed directly via pip:
```
pip install https://pypi.python.org/packages/source/p/protobuf/protobuf-3.0.0a3.tar.gz#md5=6674fa7452ebf066b767075db96a7ee0
```


Otherwise an exception like the following will occur:
```
File "[...]/googleplayupdater/googleplayupdater/gp_update.py", line 33, in <module>
    from googleplay_api.googleplay import GooglePlayAPI  # GooglePlayAPI
  File "[...]/googleplayupdater/googleplay_api/googleplay.py", line 19, in <module>
    from google.protobuf import text_format
  File "[...]/googleplayupdater/venv3/lib/python3.4/site-packages/google/protobuf/text_format.py", line 572
    except ValueError, e:
```

## Included libraries

### googleplay-api
Cloned from https://github.com/NeroBurner/googleplay-api which is a fork from https://github.com/timogilvie/googleplay-api

### AsynchronousFilereader
Cloned from https://github.com/soxofaan/asynchronousfilereader

Simple thread based asynchronous file reader for Python.

## Inspiration

Inspired by [GooglePlayDownloader](http://codingteam.net/project/googleplaydownloader) and its 'Search updates for local APK(s)'-button 

## Licence
This project is released under the AGPLv3+ licence.


