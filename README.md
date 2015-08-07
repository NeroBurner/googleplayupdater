# googleplay_updater_cli
Bulk-updater for a folder with apk-files from googleplay

## Configure
Copy the file `config_example.py` or create a new file named `config.py` and fill out your google-account information as well as your `ANDROID_ID`. Your android id can be obtained as descibed in the [googleplay-api](https://github.com/timogilvie/googleplay-api#requirements) project by using the Gtalk Manager on your phone. Or use the java program [android-checkin](https://github.com/nviennot/android-checkin).

## Synopsis
```
python2 gp_update.py [-v] <apk_folder_path>
        -v       verbose output
```

## Dependencies
This section describes the dependencies and the changes done to said dependencies.

### androguard
Cloned from: https://github.com/androguard/androguard

Using stable version 1.9.

`git checkout tags/1.9`

in the file `androguard/core/bytecodes/api.py` change the following lines

```
from androguard.core import bytecode
from androguard.core import androconf
from androguard.core.bytecodes.dvm_permissions import DVM_PERMISSIONS
```

to

```
from __future__ import absolute_import

from .. import bytecode
from .. import androconf
from .dvm_permissions import DVM_PERMISSIONS
```

### googleplay-api
Cloned from https://github.com/timogilvie/googleplay-api

in `googleplay_api/googleplay.py` change, that https-requests are verified. For all done requests replace `verify=False` with `verify=True`


## Inspiration

Inspired by [GooglePlayDownloader](http://codingteam.net/project/googleplaydownloader) and its 'Search updates for local APK(s)'-button 

## Licence
This project is released under the GPLv3 licence.


